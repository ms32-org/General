import pyvda

# Get all desktops
desktops = pyvda.get_virtual_desktops()


# Keep the first desktop
main_desktop = desktops[0]

# Loop through and remove all other desktops
for desktop in desktops[1:]:
    desktop.remove()

# Finally, switch to Desktop 1 just to be safe
main_desktop.go()

print("All extra desktops removed. Only Desktop 1 remains.")
