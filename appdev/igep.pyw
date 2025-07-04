import pyvda
from time import sleep
while True:
    # Get all desktops
    desktops = pyvda.get_virtual_desktops()

    main_desktop = desktops[0]
    if len(desktops) > 1:
        for desktop in desktops[1:]:
            desktop.remove()
        main_desktop.go()
    sleep(2)