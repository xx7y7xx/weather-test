#!/bin/bash -x

#
# download
#

curl -s -o new_radar.gif "https://weather.bangkok.go.th/Images/Radar/radar.gif"
ls -l

#
# split
#

# Split GIF into static images
convert -coalesce new_radar.gif new_radar_frame_%d.png
ls -l

# Extract timestamp and rename static images
for file in new_radar_frame_*.png; do
  # Crop the image to focus on timestamp part
  convert "${file}" -crop 120x19+838+728 "cropped_${file}"

  # $ tesseract cropped_new_radar_frame_0.png stdout -c tessedit_char_whitelist='0123456789-: ' --dpi 70 --psm 6
  timestamp=$(tesseract "cropped_${file}" stdout -c tessedit_char_whitelist='0123456789-: ' --dpi 150 --psm 6)
  if [ ! -z "$timestamp" ]; then
    mv "${file}" "radar_frame_timestamp_${timestamp}.png"
  else
    echo "timestamp not extract from file $file!"
  fi

  rm "cropped_${file}"
done
ls -l
