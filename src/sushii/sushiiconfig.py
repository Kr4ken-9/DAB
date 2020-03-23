from src import config, utils


class Sushiiconfig(config.Config):
    def __init__(self, path):
        super().__init__(path)

        self.replace_example()

    def populate_config(self, yaml_conf):
        """Populates a new config with user input via commandline

        :param yaml_conf: An example config to replace values of
        :return: A populated config
        """

        yaml_conf["firsttime"] = False

        print("\nIt looks like you haven't configured options for sushiibot yet. You can do that now or manually later.")
        repfarming = input("The first option is to farm rep from sushiibot. Enter 'True' or 'False' regarding whether or not to farm sushii rep: ")
        repfarming = utils.string_to_bool(repfarming)
        yaml_conf["repfarming"] = repfarming

        fishyfarming = input("\nNow you can choose to farm fishies or not. Enter 'True' or 'False' to farm fishies: ")
        fishyfarming = utils.string_to_bool(fishyfarming)
        yaml_conf["fishyfarming"] = fishyfarming

        if not repfarming and not fishyfarming:
            print("\nAll sushiibot related farming is disabled.")
            return yaml_conf

        channel = input("Enter the channel id to farm sushii rep and fishies: ")
        yaml_conf["channel"] = int(channel)

        repdelay = input("\nNow enter the interval, in seconds, at which rep will be farmed: ")
        yaml_conf["repdelay"] = int(repdelay)

        fishydelay = input("\nNow enter the interval, in seconds, to farm fishies: ")
        yaml_conf["fishydelay"] = int(fishydelay)

        reprecipients = []
        print("\nThe next option is who to farm sushii rep for. You can manually configure multiple recipients later.")
        reprecipients.append(int(input("Enter the id of the user to farm rep for: ")))
        yaml_conf["reprecipients"] = reprecipients

        fishyrecipients = []
        print("\nFinally, configure who to farm sushii fishies for. You can manually configure multiple recipients later.")
        fishyrecipients.append(int(input("Enter the id of the user to farm fishies for: ")))
        yaml_conf["fishyrecipients"] = fishyrecipients

        return yaml_conf
