for shape in circle hexagon pentagon plus rectangle square star trapezoid triangle
do
    if ! test -e ../hough_forests_cropped_positive_100_pos_100_neg/"$shape"_detector
    then
        mkdir -p ../hough_forests_cropped_positive_100_pos_100_neg/"$shape"_detector
    fi
    python generate_target.py shapes/"$shape".png > ../hough_forests_cropped_positive_100_pos_100_neg/"$shape"_detector/train_pos.txt
done
