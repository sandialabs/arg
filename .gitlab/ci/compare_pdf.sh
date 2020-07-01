#!/bin/bash --norc
generated_pdf=$1
standard_pdf=$2
generated_pdf_name=${generated_pdf##*/}
generated_pdf_name_wo_ext=${generated_pdf_name%.*}
standard_pdf_name=${standard_pdf##*/}
standard_pdf_name_wo_ext=${standard_pdf_name%.*}
tmp_path=.tmp_comp_pdf
exitcode=0

# Compares page count for each pdf file
generated_pdf_page_count=$(pdftk $generated_pdf dump_data | grep NumberOfPages)
standard_pdf_page_count=$(pdftk $standard_pdf dump_data | grep NumberOfPages)
if [ "$generated_pdf_page_count" != "$standard_pdf_page_count" ];
then

  echo "WARNING: The number of pages of each document is not the same:"
  echo "$generated_pdf: $generated_pdf_page_count"
  echo "$standard_pdf: $standard_pdf_page_count"

  # Exits
  exit 1
else
    echo "The number of pages of each document is the same"
fi

# Creates the temp folder
mkdir $tmp_path

# Converts the generated pdf to images (one per pdf page) (needs imagemagick)
convert $generated_pdf -strip $tmp_path/$generated_pdf_name_wo_ext-gen.png

# Converts the standard pdf to images (one per pdf page) (needs imagemagick)
convert $standard_pdf -strip $tmp_path/$generated_pdf_name_wo_ext-std.png

# Loops on find files containing *-gen-*.png sorted by name
for fgenerated in $(find $tmp_path -name "*-gen-*.png"| sort -V | xargs -r0 );
do

  # Standard images suffix
  std="-std-"

  # Replaces -gen- by -std- to find associated page in standard pdf
  fstandard=${fgenerated/-gen-/$std}

  if [ "$fgenerated" != "" ] # workaround for find command generating a blank line
  then

    # comparing images with diff
    comparison=$( diff $fgenerated $fstandard )
    status=$?

    if [ "$comparison" = "" ] && [ $status -eq 0 ];
    then
      echo "Same pages: (1):$fgenerated (2):$fstandard"
    else
      # If pages are differents, print page number and comparison result

      echo "----------------"
      echo "WARNING: Different pages:"
      echo "(1):$fgenerated (2):$fstandard"
      echo "$comparison"

      # Sets exitcode to 1 for Gitlab CI interpretation
      exitcode=1
    fi
  fi
done

# Deletes temp folder
rm -rf $tmp_path

echo "Exit $exitcode"
# Exits with the associated code
exit $exitcode
