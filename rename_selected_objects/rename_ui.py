import maya.cmds as cmds
import rename_lanh as rn
import importlib

# Refreshes the script.
importlib.reload(rn)

def rename_groups_ui():

    #Verifies for an existing window.
    window_name = "Rename UI"
    close_ui(window_name)

    # Set name variable lists.
    prefixes = ['None', 'geo_', 'ctrl_', 'rig_', 'cam_', 'lit_']
    suffixes = ['None','_char', '_prop', '_env']
    subsuffixes = [ 'None','_left', '_right', '_back', '_front' ]
    rename_inst = 'Fill this with the name of the object type. ex. Mary, mary_arm, house, etc.'
    prefix_inst = 'Select the class of object you have.'
    suffix_inst = 'Select what is this object describing. Such as enviroment prop or character light'
    subsuffix_inst = 'Select only if there is extra information needed.'
    
    # Creates the main window
    window = cmds.window(window_name, title="Rename Groups", widthHeight=(300, 180), sizeable=True)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnAlign="center")

    # Title
    cmds.text ('Rename Groups UI', align  = 'center')

    #Creates the rename field.
    cmds.textFieldGrp(
        'object_name_tfg', 
        adjustableColumn = 2,
        columnWidth = [(1,100), (3,100)],
        columnAlign = (1,'left'),
        label = 'Object Name:',
        annotation = rename_inst
                )
    
    

    #Set the Prefixes and Suffixes of the Group
    cmds.columnLayout(adjustableColumn = True, rowSpacing = 10)
    preffix_menu = cmds.optionMenuGrp('preffix_omg', 
                                    adjustableColumn = 2,
                                    columnWidth = [(1,100), (3,100)],
                                    columnAlign = (1,'left'),
                                    label = 'Class of Object:',
                                    annotation = prefix_inst
                                    )
    
    for p in prefixes:
        cmds.menuItem(label=p)

    suffix_menu = cmds.optionMenuGrp('suffix_omg', 
                                    adjustableColumn = 2,
                                    columnWidth = [(1,100), (3,100)],
                                    columnAlign = (1,'left'),
                                    label = 'Type of Object:',
                                    annotation = suffix_inst
                                    )
    
    for s in suffixes:
        cmds.menuItem(label=s)

    subsuffix_menu = cmds.optionMenuGrp('subsuffix_omg', 
                                    adjustableColumn = 2,
                                    columnWidth = [(1,100), (3,100)],
                                    columnAlign = (1,'left'),
                                    label = 'Subtype description:',
                                    annotation = subsuffix_inst
                                    )
    
    for ss in subsuffixes:
        cmds.menuItem(label=ss)
    

    cmds.separator(height=10, style='in')

    # Shows the actions buttons.
    form = cmds.formLayout()
    b1 = cmds.button(label="Rename and Close", command=lambda *args: rename_groups_close(window))
    b2 = cmds.button(label="Rename", command=lambda *args: rename_groups())
    b3 = cmds.button(label="Close", command=lambda *args: close_ui(window))

    cmds.formLayout(form, edit=True,
        attachForm=[(b1, 'left', 5), (b3, 'right', 5), (b1, 'bottom', 5), (b2, 'bottom', 5), (b3, 'bottom', 5)],
        attachControl=[(b2, 'left', 5, b1), (b3, 'left', 5, b2)],
        attachPosition=[(b1, 'right', 0, 33), (b2, 'right', 0, 66)]
                    )



    #cmds.button(label="Close", command=lambda *args: cmds.deleteUI(window))
    
    # Shows the window
    cmds.showWindow(window)

def rename_groups ():
     # Query values
    new_name = cmds.textFieldGrp('object_name_tfg', q=True, text=True)
    new_prefix = cmds.optionMenuGrp('preffix_omg', q=True, value=True)
    new_subfix = cmds.optionMenuGrp('suffix_omg', q=True, value=True)
    new_subsuffix = cmds.optionMenuGrp('subsuffix_omg', q=True, value=True)

    # Validate name input before renaming
    if not new_name or new_name.strip() == "":
        cmds.warning("Please enter a valid name before renaming.")
        return

    # Prevent illegal characters (optional but good practice)
    illegal_chars = ".|:[]{}<>()',;\"` "
    if any(c in new_name for c in illegal_chars):
        cmds.warning("Name contains illegal characters. Please remove them.")
        return

    # Safe to rename now
    tool = rn.RenamerTool(new_prefix, new_name, new_subfix, new_subsuffix)
    tool.main()

def rename_groups_close(window):
    '''
    Description:
    Renames the UI and closes the window.

    Input:
    None

    Output:
    None
    '''
    # Renames the UI.
    rename_groups()

    # Closes the window.
    close_ui(window)
    return

def close_ui (window):
    '''
    Description:
    Checks if the window exists, if it does it closes it.

    Input:
    window (str): The name of the window.

    Output:
    none
    '''
    #Gets the window name and closes it.
    window_name = window
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    return

