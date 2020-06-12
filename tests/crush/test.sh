# Execute crush case...
echo "# Testing crush case..."

# Fetch template runner from above
cp ../test-ARG-e.in test.tmp

# Substitute report name
sed -e 's/@NAME@/Report-crush/g' -i'' test.tmp 2> /dev/null ||
 # execute sed -i '' if an error occured (macOS workaround)
(sed -e 's/@NAME@/Report-crush/g' -i '' test.tmp)

# Substitute report extension
sed -e 's/@EXT@/pdf/g' -i'' test.tmp 2> /dev/null ||
 # execute sed -i '' if an error occured (macOS workaround)
(sed -e 's/@EXT@/pdf/g' -i '' test.tmp)

# Execute runner
sh test.tmp

# Get runner exitcode
exitcode=$?

# Clean up runner
rm -f test.tmp

exit $exitcode
