import copy
from jsspetri.envs.common.petri_build import Petri_build

class JSSPSimulator(Petri_build):
    """
    Class representing the core logic of a Job Shop Scheduling Problem (JSSP) simulation using a Petri net.

    Attributes:
        clock (int): The internal clock of the simulation.
        interaction_counter (int): Counter for interactions in the simulation.
        delivery_history (dict): Dictionary storing the delivery history.
        action_map (dict): Mapping for actions in the simulation from discreate to multidiscreate.

    Methods:
        __init__(instanceID): Initializes the JSSPSimulator.
        time_tick(gui, action): Increments the internal clock and updates token logging.
     
        transfer_token(origin, destination, current_clock): Transfers a token from one place to another.
        fire_colored(action): Fires colored transitions based on the provided action.
        fire_timed(): Fires timed transitions based on completion times.
        petri_interact(gui, action): Performs Petri net interactions and updates internal state.
        petri_reset(): Resets the internal state of the Petri net.
        is_terminal(): Checks if the simulation has reached a terminal state.
        action_mapping(n_machines, n_jobs): Maps multidiscrete actions to a more usable format.
        enabled_allocations(): Checks which allocations are enabled.
    """

    def __init__(self, 
                 instance_id, 
                 dynamic=False,
                 standby=False):
        """
        Initializes the JSSPSimulator.

        Parameters:
            instanceID (str): Identifier for the JSSP instance.
            dynamic (bool): If True, appending new operations is possible, and the termination condition is that all queues are empty.
        """
        super().__init__(instance_id, 
                         dynamic=dynamic,
                         standby=standby)

        self.clock = 0
        self.interaction_counter = 0
        self.delivery_history = {}
        self.machines, self.jobs, self.delivery, self.allocate, self.deliver = [], [], [], [], []
        self.petri_reset()
        
        self.job_free = [True] * self.n_jobs
        self.machine_free = [True] * self.n_machines
        self.action_map = self.action_mapping(self.n_machines, self.n_jobs)
       

    def petri_reset(self):
        """
        Resets the internal state of the Petri net.
        """
        self.clock = 0
        for place in self.places.values():
            place.token_container = []
        self.add_tokens()
   
    
        self.jobs = [p for p in self.places.values() if p.uid in self.filter_nodes("job")]
        self.allocate = [t for t in self.transitions.values() if t.uid in self.filter_nodes("allocate")]
        self.machines = [p for p in self.places.values() if p.uid in self.filter_nodes("machine")]
        self.deliver = [t for t in self.transitions.values() if t.uid in self.filter_nodes("finish_op")]
        self.delivery = [p for p in self.places.values() if p.uid in self.filter_nodes("finished_ops")]
        

    def action_mapping(self, n_machines, n_jobs):
         """
         Maps multidiscrete actions to a more versatile Discrete format to use with exp DQN.

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
                 
         if self.standby :
             idle = {len(mapping_dict.keys()): (None,None)}
             mapping_dict.update(idle)

         return mapping_dict
    

    def projected_makespan(self):
        """
        Calculates the projected makespan based on the current state.

        Returns:
            int: Projected makespan.
        """
        waiting_penalty = self.n_machines
        completion_time = [1 for _ in range(self.n_machines)]
        
        # Step 1: Estimate completion time for operations in process
        for machine in self.machines:
            if machine.token_container:
                token= machine.token_container[0]
                elapsed = token.logging[list(token.logging.keys())[-1]][2]
                remaining = token.process_time - elapsed
                completion_time[token.color[1]] = self.clock + remaining
            else:
                completion_time = [self.clock for _ in range(self.n_machines)]

        # Step 2: Assume optimal processing of remaining operations
        for job in self.jobs:
            if len(job.token_container) > 0:
                for operation in job.token_container:
                    completion_time[operation.color[1]] += operation.process_time * waiting_penalty
                    
        return max(completion_time)

    
    def utilization_reward(self):
        """
        Calculates the utilization reward.

        Returns:
            float: Calculated reward.
        """
        x = 1- (sum(self.machine_free) / self.n_machines)
        return x
    
    
    def utilization_penalty(self):
        """
        Calculates the utilization reward penalty.

        Returns:
            float: Calculated reward.
        """
        penalty_coef = 100
        x = sum(self.machine_free) / self.n_machines
        reward = (1 / penalty_coef) ** x - 1
        return reward
    
    

    def is_terminal(self, step=0):
        """
        Checks if the simulation has reached a terminal state.

        Returns:
            bool: True if the terminal state is reached, False otherwise.
        """
        empty_queue = all(len(p.token_container) == 0 for p in self.jobs)
        empty_machines = all(len(p.token_container) == 0 for p in self.machines) 
        return empty_queue and empty_machines
    
  
    def valid_action(self,action):
        valid=False
        job_idx,machine_idx=self.action_map[int(action)]
       
        if job_idx==None:
            return True    
        else :  
            
           if  self.jobs[job_idx].token_container:
            token = self.jobs[job_idx].token_container[0]
            machine = self.machines[machine_idx]
            
            color = token.color[1] == machine.color
            machine = self.machine_free[machine_idx]
            precedence = self.job_free[job_idx]  
            if color and machine and precedence:
                valid= True
                    
        return valid
    
    
    def enabled_allocations(self):
        actions = range(len (self.action_map))
        enabled_mask = list(map (self.valid_action, actions))
        
      
        return enabled_mask
        

    def time_tick(self):
        """
        Increments the internal clock and updates token logging.
        """
        self.clock += 1
        self.safeguard()
        
        for place in self.machines +self.jobs:
                if  place.token_container:
                    token = place.token_container[0]
                    last_logging = list(token.logging.keys())[-1]
                    token.logging[last_logging][2] += 1


    def transfer_token(self, origin, destination, clock=0):
        """
        Transfers a token from one place to another.

        Parameters:
            origin: Origin place.
            destination: Destination place.
            current_clock (int): Current simulation clock.
        """
        
        if not origin.token_container:# place empty 
            return False

        token = copy.copy(origin.token_container[0])
        destination.token_container.append(token)
        origin.token_container.pop(0)

        token.logging[origin.uid][1] = clock
        token.logging[destination.uid] = [clock, 0, 0]

        return True

    def safeguard(self):
        for machine in self.machines:
            if machine.token_container:
                token=machine.token_container[0]
                if machine.color != token.color[1] :
                    print(f"error detected { (machine.color, token.color[1])}")
                   

    def fire_colored(self, action):
        """
        Fires colored transitions based on the provided action.

        Parameters:
            action: Action to be performed.

        Returns:
            bool: True if a transition is fired, False otherwise.
        """
        self.interaction_counter += 1
        job_idx, machine_idx = self.action_map[int(action)] 
        
        if job_idx == None :
            return True  #handle standby action
        
        elif action in [index for index, value in enumerate(self.enabled_allocations()) if value]: 
            fired = self.transfer_token(self.jobs[job_idx], self.machines[machine_idx], self.clock)    
            self.job_free[job_idx] = False
            self.machine_free[machine_idx] = False 
            return fired
        
        else:
            return False
       

    def fire_timed(self):
        """
        Fires autonomous transitions based on completion times.
        """
        fired = False
        
        for  machine in self.machines: 
            if machine.token_container:
                token = machine.token_container[0]
                _, _, elapsed_time = list(token.logging.items())[-1][-1]
                if  elapsed_time> token.process_time  :
                    self.transfer_token(machine, self.delivery[machine.color], self.clock)
                    self.job_free[token.color[0]] = True
                    self.machine_free[token.color[1]] = True 
                    fired = True
                    
        self.time_tick()          
        self.delivery_history[self.clock] = [token for place in self.delivery for token in place.token_container]
        
        return fired

    def interact(self, action):
        
        """
        Performs Petri net interactions and updates internal state.

        Parameters:
            action: Action to be performed.
        """

        fired=self.fire_colored(action)
        self.fire_timed()

        # Only the idle is enabled (no action available)
        while sum(self.enabled_allocations()) == int (self.standby):
            self.fire_timed()
            if self.is_terminal():
                break
            
        return fired

if __name__ == "__main__":
    
    sim = JSSPSimulator("ta01",dynamic=False,standby=True)
     
    print(sim.action_map)
    print(sim.enabled_allocations())


    # print(len(sim.machine_free))
    # print(len(sim.job_free))
    # print(len (sim.machines))
    # print(len (sim.jobs))
    # print(len (sim.allocate))
    # print(len (sim.deliver))
    
    # print([machine.color for machine in sim.machines])
    # print([job.color for job in sim.jobs])
    
    # print([len (machine.token_container) for machine in sim.machines])
    # print([len (job.token_container) for job in sim.jobs])
    
    # print(len (sim.action_map))
    # print(sim.action_map)
    
    # print("*---------------------------------------------------------------")
    
    # print(sim.job_free)
    # print(sim.machine_free)
    
   
    # print([len (job.token_container) for job in sim.jobs])
    # print([len (machine.token_container) for machine in sim.machines])
    # print([len (delivery.token_container) for delivery in sim.delivery])
 
    
    # sim.fire_colored(17)
    
   
    # print([len (job.token_container) for job in sim.jobs])
    # print([len (machine.token_container) for machine in sim.machines])
    # print([len (delivery.token_container) for delivery in sim.delivery])
    
    # print(sim.job_free)
    # print(sim.machine_free)
    
    # sim.fire_timed()
    
    # print([len (job.token_container) for job in sim.jobs])
    # print([len (machine.token_container) for machine in sim.machines])
    # print([len (delivery.token_container) for delivery in sim.delivery])
    
    # print(sim.job_free)
    # print(sim.machine_free)
    
    
    


    
    
    
   

    



    
    
    
   

    
