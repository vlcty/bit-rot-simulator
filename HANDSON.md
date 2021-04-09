# Hands on

You'll find a vagrant config file in this repository to test it out safely. It'll spin up a VM with three hard drives, creates a btrfs RAID1 for data and metadata and mount it to /tmp.

    VAGRANT_EXPERIMENTAL="disks" vagrant up

After it boots up you can ssh into the box

    vagrant ssh

And get to a root shell:

    sudo -i

Execute the following command and wait until it finishes:

    /vagrant/create-random-data.sh

It'll create files with random data on the mounted btrfs file system. Then it's time to start the first scrub:

    [root@archlinux ~]# btrfs scrub start -B /mnt
    scrub done for aafdf71d-269f-4f41-aa3c-0fefc15a1754
    Scrub started:    Fri Apr  9 16:51:57 2021
    Status:           finished
    Duration:         0:00:05
    Total to scrub:   5.66GiB
    Rate:             993.93MiB/s
    Error summary:    no errors found

As expected nothing wrong ... yet! Time to let the bits rot:

    [root@archlinux ~]# /vagrant/bitrot.py /dev/sdb1
    Warning: Random bytes will be written to /dev/sdb1! Are you sure you want to continue?
    Please type uppercase YES if you know what you are doing: YES
    Position: 0/2145911296 -> 0.0% done
    Position: 614343511/2145911296 -> 28.63% done
    Position: 1228002599/2145911296 -> 57.23% done
    Position: 1842554690/2145911296 -> 85.86% done
    Position: 2145911296/2145911296 -> 100.0% done

And scrub afterwards:

    [root@archlinux ~]# btrfs scrub start -B /mnt
    scrub done for aafdf71d-269f-4f41-aa3c-0fefc15a1754
    Scrub started:    Fri Apr  9 16:55:22 2021
    Status:           finished
    Duration:         0:00:53
    Total to scrub:   5.66GiB
    Rate:             93.77MiB/s
    Error summary:    csum=132766
      Corrected:      132766
      Uncorrectable:  0
      Unverified:     0
    WARNING: errors detected during scrubbing, corrected

Seems like the errors were corrected! btrfs seems to work.

# More to test

There are more tests you can do on your own.

## Reading without a scrub

Does reading from the file system also heal itself when no scrub happens?

1) Take the SHA256 sum of a couple of files
2) Let the bits rot
3) Take the SHA256 sums again. Do they differ?
4) Does dmesg log something?

## How do multiple rotting partitions affect btrfs RAID 1?

RAID 1 stores one copy. So rotting one drive apparently has no effect. What happens when you rot two partitions? Does the scrub output change? Does is change the outcome when you use raid1c3 instead of raid1?
