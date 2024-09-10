from mcrcon import MCRcon

def send_rcon_command(command: str):
    with MCRcon("YOUR_SERVER_IP", "YOUR_RCON_PASSWORD") as mcr:
        response = mcr.command(command)
        return response