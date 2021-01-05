# shiny_counter
App to help keep track of shiny hunting attempts in Pokemon


How to use:

Run counter.py program. Counter will appear in a corner of your screen. 

Initial value will be set to the value in *savedata.txt*.

Font/Size of figure will be determined via the *style.json* file.

You can reconfigure which corner the text appears on by modifying the *style.json* file.

Pressing + will increment counter by 1. Pressing - will decrement counter by 1. Pressing * will reset counter to 0

Pressing the | (pipe character) will allow you access to additional inputs including:

    qqq (press q 3 times) - Close the counter program. This saves the current counter value in *savedata.txt*.
    
    f - brings up dialoge box so you can modify the font size while program is running.
    
    . - allows you to set the counter to a value you want. Make sure to set counter to 0 before doing this, then type in desired number.
    
        If you mess up, set counter to 0 again and try again.
        
    p - toggles reposition the counter using the arrow keys.
    
    r - loads the counter value currently saved in *savedata.txt*.
    
    s - saves the current counter value to *savedata.txt*.
    
