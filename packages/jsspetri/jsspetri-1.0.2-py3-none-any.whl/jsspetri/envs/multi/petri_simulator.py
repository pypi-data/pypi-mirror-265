import copy
import random
import numpy as np
from jsspetri.envs.common.petri_build import Petri_build


class JSSPSimulator(Petri_build):
    """
    Class representing the core logic of a Job Shop Scheduling Problem (JSSP) simulation using a Petri net.

    Attributes:
        internal_clock (int): The internal clock of the simulation.
        interaction_counter (int): Counter for interactions in the simulation.
        total_internal_steps (int): Total internal steps taken in the simulation.
        delivery_history (dict): Dictionary storing the delivery history.
        action_map (dict): Mapping for actions in the simulation.

    Methods:
        __init__(instanceID): Initializes the JSSPSimulator.
        time_tick(gui, action): Increments the internal clock and updates token logging.
        filter_nodes(node_type): Filters nodes based on node type.
        transfer_token(origin, destination, current_clock): Transfers a token from one place to another.
        fire_colored(action): Fires colored transitions based on the provided action.
        fire_timed(): Fires timed transitions based on completion times.
        petri_interact(gui, action): Performs Petri net interactions and updates internal state.
        petri_reset(): Resets the internal state of the Petri net.
        projected_makespan(): Calculates the projected makespan based on the current state.
        is_terminal(): Checks if the simulation has reached a terminal state.
        action_mapping(n_machines, n_jobs): Maps multidiscrete actions to a more usable format.
        enabled_allocations(): Checks which allocations are enabled.
    """

    def __init__(self, instance_id,dynamic=False):
        """
        Initializes the JSSPSimulator.

        Parameters:
            instanceID (str): Identifier for the JSSP instance.
            dynamic (bool) : if True, a petrinet with 100*200  container is created regardless the actual instance size 
        """
        super().__init__(instance_id,dynamic)
        
        self.dynamic=dynamic
        self.internal_clock = 0
        self.interaction_counter = 0
        self.relatif_clock=[]  # contain the absolute time step for every interaction
        
        self.delivery_history = {}
        self.machines_busy=np.zeros(self.n_machines) 
        self.machines_idle=np.zeros(self.n_machines)
        
        
        self.target_consumption=0
        self.energy_consumption=[]
        self.max_consumption,self.min_consumption=(0,0)
        
 
        if self.dynamic :
            self.action_map=self.action_mapping(self.max_nmachines, self.max_njobs)
        else :
            self.action_map = self.action_mapping(self.n_machines, self.n_jobs)
            
            
        self.machines=[p for p in self.places.values() if p.uid in self.filter_nodes("machine")]
        self.jobs =[p for p in self.places.values() if p.uid in self.filter_nodes("job")]
        self.delivery=[p for p in self.places.values() if p.uid in self.filter_nodes("finished_ops")]
        self.allocate=[t for t in self.transitions.values() if t.uid in self.filter_nodes("allocate")]
        self.deliver=[t for t in self.transitions.values() if t.uid in self.filter_nodes("finish_op")]
        self.action_map = self.action_mapping(self.n_machines, self.n_jobs)


    def time_tick(self):
        """
        Increments the internal clock and updates token logging.
        Parameters:
            action: Action to be performed.
        """
        self.clock += 1
        for machine in self.machines:
            try :
                token = machine.token_container[0]
                last_logging = list(token.logging.keys())[-1]
                token.logging[last_logging][2] += 1  
            except:
                pass
            
    def transfer_token(self, origin, destination, clock=0):
        """
        Transfers a token from one place to another.

        Parameters:
            origin: Origin place.
            destination: Destination place.
            current_clock (int): Current simulation clock.
            fifo the oldest position 0 the newest -1
            # entry time, leave time, elapsed time
            
        """
        
        if not origin.token_container:
            #print("Error: Origin token container is empty.")
            return False

        token = copy.copy(origin.token_container[0])
        destination.token_container.append(token)
        origin.token_container.pop(0)
        
        token.logging[origin.uid][1] = clock
        token.logging[origin.uid][2] = clock-token.logging[origin.uid][0]
        token.logging[destination.uid] = [clock, 0, 0]   

        return True
                
    def fire_colored(self, action):
        """
        Fires colored transitions based on the provided action.
        Parameters:
            action: Action to be performed.

        Returns:
            bool: True if a transition is fired, False otherwise.
             
        """
        
        if self.enabled_allocations()[action]:
        
            self.interaction_counter += 1
            job_idx,machine_idx= self.action_map[int(action)] 
            fired =self.transfer_token(self.jobs[ job_idx], self.machines[machine_idx],self.clock)
            
            self.machine_free[machine_idx]=False
            self.job_free[job_idx]=False
            return fired
            
        else:  
            return False

    
        

    def fire_timed(self):
        """
        Fires autonomous transitions based on completion times.
        """
        fired = False
        
        for machine_index, machine in enumerate(self.machines):
            try:
                token = machine.token_container[0]
                _, _, elapsed_time = list(token.logging.items())[-1][-1]
    
                if token.process_time <= elapsed_time:
                    self.transfer_token(machine, self.delivery[machine.color], self.clock)  
                    self.job_free[token.color[0]] = True
                    self.machine_free[token.color[1]] = True
                    fired = True
            except IndexError:
                pass
    
        # Keep a history of delivery (to use in solution later)
        self.delivery_history[self.clock] = [token for place in self.delivery for token in place.token_container]
        
        
        return fired
        
        
    def petri_reset(self):
        """
        Resets the internal state of the Petri net.
        """
        self.internal_clock = 0
        for place in self.places.values():
            place.token_container = []
        # Add tokens
        self.add_tokens()
        
    
    def Energy_Reward(self):   
            
            consumption = 0
            np.random.seed(101)
            machines_powers = np.random.randint(10, 100, size=self.n_machines)
            
            usage_cap= 0.1
            self.min_consumption=min (machines_powers)
            self.max_consumption=machines_powers.sum()
            
            self.target_consumption =usage_cap * machines_powers.sum()

            machine_places = [p for p in self.places.values() if p.uid in self.filter_nodes("machine")]
            for machine in machine_places:
                if len(machine.token_container) > 0:
                    consumption += machines_powers[machine.color] 
                    
            deviation= consumption-self.target_consumption
            x= (deviation/self.target_consumption)*0.1
            
            overshoot_coef=100
            undershoot_coef=1e6 # bigger means less tolerant with the deviation


            if deviation < 0 :     
                reward= undershoot_coef**x -1  
            else :       
                reward= (1/overshoot_coef)**x -1 
            
            if  consumption == 0 :
                reward = -2
                
            return reward, consumption
        

    def Utilization_Reward(self): 

        machine_places = [p for p in self.places.values() if p.uid in self.filter_nodes("machine")]
        idle_machines = sum(1 for machine in machine_places if len(machine.token_container) == 0)
       
        penalty_coef=100
        x =  idle_machines / self.n_machines
        reward= (1/penalty_coef)**x -1 
        return reward


    def is_terminal(self,step=0):
        """
        Checks if the simulation has reached a terminal state.
         is terminal if all the machines and queues are empty 

        Returns:
            bool: True if the terminal state is reached, False otherwise.   
        """

        empty_queue= all(len(p.token_container)==0 for p in self.jobs)
        empty_machines = all(len(p.token_container)==0 for p in self.machines)

        return  empty_queue and  empty_machines 



    
    def enabled_allocations(self,pre_const=True):
        """
        Determine the enabled allocations based on the current state of the Petri net.
    
        Returns:
            list: A list indicating which allocations are enabled. True for enabled, False otherwise.
        """
        
        enabled_mask = [False] * len(self.action_map) 
        for key, (job_index, machine_index) in self.action_map.items():
               
            if not self.jobs[job_index].token_container: #check if the queue is empty 
                continue 
            
            token = self.jobs[job_index].token_container[0]  # fist token in the que
            allocation = self.allocate[machine_index]
            
            #constrains
            color = token.color[1] == allocation.color
            machine = self.machine_free[machine_index]
            precedence = self.job_free[job_index] if pre_const else True

            if color and machine and precedence:
                enabled_mask[key] = True
    
        return enabled_mask 
    
    
    def action_mapping(self, n_machines, n_jobs):
        """
        Maps multidiscrete actions to a more versatile Descrite format to use with exp DQN.

        Parameters:
            n_machines (int): Number of machines.
            n_jobs (int): Number of jobs.

        Returns:
            dict: Mapping dictionary.
        """
        tuples = []
        mapping_dict = {}

        for machine in range(n_machines):
            for job in range(n_jobs):
                tuple_entry = (job, machine)
                tuples.append(tuple_entry)
                index = len(tuples) - 1
                mapping_dict[index] = tuple_entry
     
        return mapping_dict

    def interact(self, action):
        """
        Performs Petri net interactions and updates internal state.

        Parameters:
            gui: User interface (if available).
            action: Action to be performed.

        Returns:
            predited  makespan or other objectif.
            
        """
        
        self.fire_timed()
        self.fire_colored(action)
        self.time_tick(action)
        self.relatif_clock.append(self.internal_clock)
        # Only the idle is enabled (no action available)
       
        while sum(self.enabled_allocations()) == 0:
            self.fire_timed()
            self.time_tick( action)
            if self.is_terminal():
                break

        energy_reward,consumption=self.Energy_Reward() 
        utilization_reward=self.Utilization_Reward()
        self.energy_consumption.append(consumption)
           
        feed_backs=[utilization_reward, energy_reward]

        return  feed_backs

    
if __name__ == "__main__":
    
    sim = JSSPSimulator("ta01")

    

 