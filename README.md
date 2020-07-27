# Py2DF

A modern, easy to use and feature-rich tool to convert written, easier to understand python code to a DiamondFire template.

==========

Installing
----------

**Python 3.6 or higher is required**

To install the library you can just run the following command:  THIS ISN'T LIVE YET BUT WILL BE SOON TM

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U Py2DF.py

    # Windows
    py -3 -m pip install -U Py2DF.py


Quick Example
--------------

.. code:: py

    @PlayerEvent.Join
    def on_join():
        p_default.send_messsage("Test")
        p_default.give_items(Item(material=material.DIAMOND_SWORD, name="My Sword", lore=["My custom sword]))
        p_default.teleport(Location(50, 50, 50))
        


You can find more examples in the examples directory.

Links
------

- `Documentation <https://py2df.readthedocs.io/en/latest/index.html>`_
- `Official Discord Server <https://discord.gg/eUVVRyE>`_
