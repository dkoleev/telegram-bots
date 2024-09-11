from mcrcon import MCRcon

def send_rcon_command(command: str):
    with MCRcon("YOUR_SERVER_IP", "YOUR_RCON_PASSWORD") as mcr:
        response = mcr.command(command)
        return response
    
def check_raid_events():
    with MCRcon("YOUR_SERVER_IP", "YOUR_RCON_PASSWORD") as mcr:
        response = mcr.command("get log")  # Example: Fetch logs or any other command to track raid events
        return response
    
def is_raid_detected(log_data):
    # Check if any logs contain keywords that signify a raid
    raid_keywords = ["C4", "rocket", "explosion", "building destroyed"]
    
    for line in log_data.splitlines():
        if any(keyword in line for keyword in raid_keywords):
            return True, line  # Return true and the matching log line
    return False, None