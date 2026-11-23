#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>

#define N 4
#define M 4

typedef int32_t** Matrix;
typedef int32_t* Row;
typedef int32_t El;

Matrix alloc_matrix(size_t n, size_t m);
void free_matrix(Matrix matrix, size_t width);

void input_matrix(Matrix, size_t width, size_t length);
void print_matrix(Matrix, size_t width, size_t length);

Matrix mult_matrix(Matrix a, Matrix b, size_t width, size_t length);


Matrix power_matrix(Matrix a, size_t power, size_t width, size_t length) {
    Matrix result = alloc_matrix(width, sizeof(Row));

    if (result == NULL) {
        perror("Allocate memory");
        return NULL;
    }

    for (size_t i = 0; i < width; ++i) {
        for (size_t j = 0; j < length; ++j) {
            if (i == j) {
                result[i][j] = 1;
            }
        }
    }

    while (power != 0) {
        if (power % 2 != 0) {
            result = mult_matrix(result, a, width, length);
        }
        a = mult_matrix(a, a, width, length);
        power /= 2;
    }

    return result;
}


int main(void) {
    Matrix matrix = alloc_matrix(N, sizeof(Row));

    if (matrix == NULL) {
        return EXIT_FAILURE;
    }

    input_matrix(matrix, N, M);
    print_matrix(matrix, N, M);

    size_t power;
    printf("В какую степень возвеcти: ");
    scanf("%zu", &power);

    Matrix res = power_matrix(matrix, power, N, M);

    printf("\nA^%zu:\n", power);
    print_matrix(res, N, M);

    free_matrix(matrix, N);
    free_matrix(res, N);

    return EXIT_SUCCESS;
}


Matrix alloc_matrix(size_t n, size_t m) {
    Matrix matrix = calloc(n, m);

    if (matrix == NULL) {
        perror("Allocate memory");
        return NULL;
    }

    for (size_t i = 0; i < n; ++i) {
        matrix[i] = calloc(m, sizeof(El));
        if (matrix[i] == NULL) {
            perror("Allocate memory");
            return NULL;
        }
    }

    return matrix;
}


void free_matrix(Matrix matrix, size_t length) {
    for (size_t i = 0; i < length; ++i) {
        free(matrix[i]);
    }

    free(matrix);
}


void input_matrix(Matrix mat, size_t width, size_t length) {
    for (size_t i = 0; i < width; ++i) {
        for (size_t j = 0; j < length; ++j) {
            printf("Mat[%zu][%zu]: >>> ", i, j);
            scanf("%" SCNd32, &mat[i][j]);
        }
    }
}


void print_matrix(Matrix mat, size_t width, size_t length) {
    for (size_t i = 0; i < width; ++i) {
        putchar('[');
        for (size_t j = 0; j < length; ++j) {
            printf("%7" PRId32 "%s", mat[i][j], (j == length - 1) ? "": ", ");
        }
        puts("]");
    }
}


Matrix mult_matrix(Matrix a, Matrix b, size_t width, size_t length) {
    Matrix result = alloc_matrix(N, sizeof(Row));

    if (result == NULL) {
        perror("Allocate memory");
        return NULL;
    }

    for (size_t i = 0; i < width; ++i) {
        for (size_t j = 0; j < length; ++j) {
            for (size_t k = 0; k < length; ++k) {
                result[i][j] += a[i][k] * b[k][j];
            }
        }
    }

    return result;
}
