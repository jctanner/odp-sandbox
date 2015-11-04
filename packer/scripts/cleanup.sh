#!/bin/bash -eux

# Zero out the rest of the free space using dd, then delete the written file.
echo "Zero'ing out the rest of the disk ..."
dd if=/dev/zero of=/EMPTY bs=1M
echo "Deleting zero'ed tempfile ..."
rm -f /EMPTY

# Add `sync` so Packer doesn't quit too early, before the large file is deleted.
echo "Sync'ing to disk"
sync
