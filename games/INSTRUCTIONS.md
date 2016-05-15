Making Your Own AVE Game
------------------------

To make your own AVE game, have a look at the examples
in this folder. At some point this help file will be
more helpful...

Rooms are started with #. There must be a space following this and then the unique ID of the room.

Text that will appear describing the room for the player should be place on the following lines.

Options for the user should follow the format:

    Description of option => room_id

Where room_id is the ID of the room that the player will be sent to.

Items can be added to a users inventory with the + symbol at the end of a line. This can follow either a description line (in which case the item will be added as soon as the user enters the room) or to an option line, in which case the item will be added before entering the next room. For example:

    Here is a bucket. + bucket

will add a bucket to the players inventory.

Options and lines of dialog can be conditionally displayed based upon items in the players inventory. For example:

    Hello there ? bucket

will only be displayed if the user already has the bucket in their inventory. Whereas:

    Goodbye ?! bucket

will only be displayed if the player does not have a bucket in their dictionary.

The '+', '?', and '?!' symbols must have leading and trailing whitespace in order to function, so it is possible to have questions in your script.

Items can be described in your game file using the '%' key. Similar to the '#' key for rooms, there must be a space following the key and then the item id. For example:

    % bucket
    Empty Bucket

Will display the bucket in the user's inventory as "Empty Bucket". The '?' and '?!' can be used for items as well so:

    % bucket
    Empty Bucket !? water
    Full Bucket ? water

Will change the display name of an item depending on the presence of water in the player's inventory. Only the first 18 characters will be displayed in the player's inventory.

If you need to check whether the player has an empty or a full bucket, you will need to check both item ID's:

    You need water in the bucket. ? bucket ?! water

Have fun writing amazing games.
