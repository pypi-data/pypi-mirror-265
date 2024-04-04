IDSPy Toolkit
=============

This module contains a serie of function to help mange and manipulate IDSPy dataclasses

 * fill_missing_values
 * ids_to_hdf5
 * hdf5_to_ids
 * get_ids_value_from_string
 * set_ids_value_from_string
 * list_ids_members
 * copy_ids


**Please note that this work is still under progress/heavy development and as experimental status.
This means that functions arguments/signatures as long as HDF5 structure might be totally redesigned in the next updates.**

## Quick example
#################################################################################################
.. code-block:: python
   :number-lines:

    import pprint
    import dataclasses

    import idspy_toolkit
    from idspy_dictionaries import ids_gyrokinetics

    pp = pprint.PrettyPrinter(indent=2)

    ids_test = ids_gyrokinetics.Gyrokinetics()
    # you can directly print the class to see what it looks like  :
    pp.pprint(ids_test)

    # if you want to see all the available classes in the current module :
    ids_dict = idspy_toolkit.list_ids_members(gkids)
    pp.pprint(ids_dict)

    #to fill an IDS with default values
    idspy_toolkit.fill_missing_values(ids_test)

    # you can use the . to access ids members :
    pp.pprint(ids_test.ids_properties)

    # and to set a value :
    ids_test.ids_properties.comment="a comment"

    # if in a script you want to reach a "deeper" value, you can use the function *get_ids_value_from_string*
    idspy_toolkit.get_ids_value_from_string(ids_test, "ids_properties/comment")
    # and for list element, put the element index after an #
    idspy_toolkit.get_ids_value_from_string(ids_test, "tag#0/name")

    # same kind of function exist to set a value :
    idspy_toolkit.set_ids_value_from_string(ids_test, "tag#0/name", "a new tag name")

    # pour afficher la classe sous forme de dictionnaire (conseil mettez l'ecran en vertical ;)):
    ids_dict = dataclasses.asdict(ids_test)
    pp.pprint(ids_dict)
