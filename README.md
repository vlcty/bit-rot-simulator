# bit-rot-simulator

Your file system claims to be able to detect and fix bitrot? Have you ever tested it? Now you have the chance to test it! This script will seek through your raw device file and write random bytes to random positions.

## Usage

Call the script and pass the partition to manipulate:

    ./bitrot.py /dev/sdd1

**Note**: You must run this script with root privileges!

It will ask you for confirmation and then start doing it's job. Example run:

    [root@archlinux ~]# python /vagrant/bitrot.py /dev/sdd1
    Warning: Random bytes will be written to /dev/sdd1! Are you sure you want to continue?
    Please type uppercase YES if you know what you are doing: YES
    Position: 0/2145911296 -> 0.0% done
    Position: 614498843/2145911296 -> 28.64% done
    Position: 1229449712/2145911296 -> 57.29% done
    Position: 1844993959/2145911296 -> 85.98% done
    Position: 2145911296/2145911296 -> 100.0% done

Done! Start a scrub to see if the errors are detected. Do you have the balls to test it out on your prod filesystem? If not see HANDSON.md if you want to play around with btrfs in a VM.

## How it works

The actual application is fairly simple:

1) It opens your specified device file
2) It seeks to a random position
3) It writes a couple of bytes to that position
4) Repeats step 2 and 3 until the end of that partition is reached

You can tweak the seek offset and amount of written bytes by editing the script. It's very simple and easy to understand. I'm not a python developer at all any I was able to easily write it.

This script has not third party dependencies. Developed against Python 3.9.2.
