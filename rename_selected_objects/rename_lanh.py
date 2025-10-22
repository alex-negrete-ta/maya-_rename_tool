import maya.cmds as cmds

class RenamerTool:
    '''
    Description:
    Is a class tool that renames the selection in maya, versions up and checks if group.
    
    Input:
    prefix (str): The class preffixx. ex. geo_,lit_, etc.
    base_name (str): The name of the selection.
    suffix(str): The type of object description. ex. enviroment(_env_), character (_char_), etc.
    subsuffix(str): Extra description in case needed. ex. _left_,_right_,_top_,_etc.

    Output:
    rename (str): A new name for the selection
    '''
    def __init__(self, prefix='None', base_name='object', suffix='None', subsuffix = 'None'):
        self.prefix = prefix if prefix != 'None' else ''
        self.base_name = base_name
        self.suffix = suffix if suffix != 'None' else ''
        self.subsuffix = subsuffix if subsuffix != 'None' else ''

    def main(self):
        '''
        Description:
        Executes the class.

        Input:
        None

        Ouput:
        rename (str): A new name for the selection.
        '''
        # Grabs the selection.
        sel = cmds.ls(selection=True)

        # Verifies the selection.
        if not sel:
            cmds.warning("No objects selected to rename.")
            return
        
        # Checks if there are multiple selections and only versions up if it does.
        if len(sel) > 1:   
            for i, obj in enumerate(sel, start=1):
                # Build version suffix (e.g., _001)
                version = f"_{len(sel)-i:03d}"
        else:
            version = ''

        # Creates the new name.
        new_name = f"{self.prefix}{self.base_name}{self.suffix}{self.subsuffix}{version}"

        #Checks if its a group.
        for obj in sel:
            node_type = cmds.nodeType(obj)
            children = cmds.listRelatives(obj, children=True)

              # Detect if it's a group (transform with at least one transform child)
            is_group = node_type == 'transform' and any(cmds.nodeType(c) == 'transform' for c in children)
            print(f"Renaming {obj} to '{new_name}'")

            # Checks if its a group, and if so it renames it to group or object.
            if is_group:
                new_group_name = f"{new_name}_grp"
                rename = cmds.rename(obj, new_group_name)
            else:
                rename = cmds.rename(obj, new_name)
            
            print(f"Renamed: {obj} → {rename}")
        
        return rename

        
'''
# Example usage
if __name__ == "__main__":
    tool = RenamerTool(prefix='geo_', base_name='lamp', suffix='_char_')
    tool.main()
'''