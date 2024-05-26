from modules import ModulesManager

AdminModule: ModulesManager = ModulesManager("group")
AdminModule.connect("modules.admin", "panel")
AdminModule.connect("modules.admin", "statistics")
AdminModule.connect("modules.admin", "mailing")
AdminModule.connect("modules.admin", "constants")
