from src import config, utils


class Kohaippconfig(config.Config):
    def __init__(self, path):
        super().__init__(path)

        self.replace_example()

    def populate_config(self, yaml_conf):
        """Populates a new config with user input via commandline

        :param yaml_conf: An example config to replace values of
        :return: A populated config
        """

        yaml_conf["firsttime"] = False

        print("\nIt looks like you haven't configured options for kohaipp yet. You can do that now or manually later.")
        enabled = input("Enter 'True' or 'False' to enable or disable kohaipp farming for the time being: ")
        enabled = utils.string_to_bool(enabled)
        yaml_conf["enabled"] = enabled

        if not enabled:
            print("\nKohaipp farming has been disabled.")
            return yaml_conf

        print("\nThe first kohaipp feature you can automate is begging. You can beg for gold at any pp size.")
        begging = input("Enter 'True' or 'False' to enable/disable automating begging: ")
        begging = utils.string_to_bool(begging)
        yaml_conf["begging"] = begging

        print("\nThe second kohaipp feature you can automate is raid. You can raid at any pp size.")
        raiding = input("Enter 'True' or 'False' to enable/disable automating raiding: ")
        raiding = utils.string_to_bool(raiding)
        yaml_conf["raiding"] = raiding

        print("\nThe third kohaipp feature you can automate is mining. You can begin mining at 20k+ pp size.")
        mining = input("Enter 'True' or 'False' to enable/disable automating mining: ")
        mining = utils.string_to_bool(mining)
        yaml_conf["mining"] = mining

        print("\nThe fourth kohaipp feature you can automate is pet bonding. You can bond whenever you get a pet.")
        bonding = input("Enter 'True' or 'False' to enable/disable automating bonding: ")
        bonding = utils.string_to_bool(bonding)
        yaml_conf["bonding"] = bonding

        print("\nNow we need to configure a channel to automate kohaipp in.")
        print("You can manually assign a specific channel for each operation, right now we will use one channel for all operations.")
        channel = input("Enter the channel id to automate kohaipp in: ")
        yaml_conf["begchannel"] = int(channel)
        yaml_conf["raidchannel"] = int(channel)
        yaml_conf["minechannel"] = int(channel)
        yaml_conf["bondchannel"] = int(channel)

        print("\nIntervals for each automation are automatically set to be compatible with Kohaipp cooldowns.")
        print("However, you can tweak these manually.")

        return yaml_conf
