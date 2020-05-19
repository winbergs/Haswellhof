#include "integral_image.h"

#include <stdio.h>

// Creates the struct of the integral image with empty data
struct integral_image *create_integral_img(int width, int height) {
    
    // Allocating memory to integral image that is returned
    struct integral_image *iimage = (struct integral_image *)malloc(sizeof(struct integral_image));
    
    // Setting real image width and height
    iimage->width = width;
    iimage->height = height;
    
    // Setting data width and height to be same as normal width and height
    // since this integral image has no padding
    iimage->data_width = width;
    iimage->data_height = height;

    // Allocating data for storing values of integral image
    iimage->padded_data = (float *)malloc(width * height * sizeof(float));
    
    // Setting data and padded data to be equal since this integral image has no padding
    iimage->data = iimage->padded_data;

    return iimage;

}

// Computes the integral image
void compute_integral_img(float *gray_image, struct integral_image *iimage) {
    
    float row_sum = 0.0f;

    float *iimage_data = iimage->data;
    int data_width = iimage->data_width;
    int width = iimage->width;
    int height = iimage->height;

    /* sum up the first row */
    for (int i = 0; i < width; i++) {
        /* previous rows are 0 */
        row_sum += gray_image[i];
        iimage_data[i] = row_sum;
    }

    /* sum all remaining rows*/
    for (int i = 1; i < height; ++i) {
        row_sum = 0.0f;
        for (int j = 0; j < width; ++j) {
            row_sum += gray_image[i * width + j];
            /*add sum of current row until current idx to sum of all previous rows until current index */
            iimage_data[i * data_width + j] = row_sum + iimage_data[(i - 1) * data_width + j];
        }
    }
}
