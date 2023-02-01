
# CPU consumption model
# Total Consumption = Idle power consumption + Utilization * (TDP - Idle power consumption)
# P_c = P_i + U * (TDP - P_i) (same as above)
# We run our software in a serverless cloud environment where we can assume that the utlizatino is 
# nesr 100%. Therfore the Idle power draw cancles out and we are only interested
# in the max power draw of a CPU.
# Assuming CPU power draw of 5.5W
# Energy, then, is total consumption * time spent
# E = P_c * d_t
def energy_from_cpu(cpu_time):
    return 5.5 * cpu_time


# RAM consuption
# we assume about 3W/8GB = 0.375W/GB of RAM
# source: https://www.tomshardware.com/reviews/intel-core-i7-5960x-haswell-e-cpu,3918-13.html
# Again, we assume that the cloud vendor exacty matches the ram requirement
# E = P_ram * d_t
def energy_from_memory_use(ram_gb_max, time):
    return (0.375 * ram_gb_max) * time


# Disk consuption
# We assume that the application is such that disk is insignificant in the kinds of tasks we
# are testing.
def energy_from_disk_use(time):
    return 0

#Network consumption
# We assume that the cloud vendor exacty matches the network requirement
# Assume power intensiy is 0.06 kWh/GB = 0.06 * 3600000 J (or Ws) of network (https://onlinelibrary.wiley.com/doi/10.1111/jiec.12630)
# this likely an overestimate
def energy_from_network_use(gb_sent, gb_received):
    return (gb_sent + gb_received) * (0.06 * 3600000)
