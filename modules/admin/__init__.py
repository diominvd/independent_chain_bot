from modules import ModulesManager

AdminModule: ModulesManager = ModulesManager("admin")
AdminModule.connect("modules.admin", "database")
AdminModule.connect("modules.admin", "messages")
AdminModule.connect("modules.admin", "panel")