#include "data_struct.h"
#include <stdio.h>

// Create integer data
struct Data *createIntData(int value) {
    struct Data *data = (struct Data *) malloc(sizeof(struct Data));
    data->type = INTEGER;
    data->value.intValue = value;
    return data;
}

// Create string data
struct Data *createStringData(char *value) {
    struct Data *data = (struct Data *) malloc(sizeof(struct Data));
    data->type = STRING;
    data->value.stringValue = strdup(value);
    return data;
}

// Create array data
struct Data *createArrayData(struct Data** items, size_t length) {
    struct Data *data = (struct Data *) malloc(sizeof(struct Data));
    data->type = ARRAY;
    data->value.dataArray.items = items;
    data->value.dataArray.length = length;
    return data;
}

// Create nested data
struct Data *createNestedData(struct Data *nested) {
    struct Data *data = (struct Data *) malloc(sizeof(struct Data));
    data->type = NESTED;
    data->value.nestedData = nested;
    return data;
}

void printData(struct Data *data) {
    switch (data->type) {
        case INTEGER:
            printf("%d\n", data->value.intValue);
            break;
        case STRING:
            printf("%s\n", data->value.stringValue);
            break;
        case NESTED:
            printData(data->value.nestedData); // Recursive call
            break;
    }
}

void freeData(struct Data *data) {
    if (data->type == STRING) {
        free(data->value.stringValue);
    } else if (data->type == NESTED) {
        freeData(data->value.nestedData);
    } else if (data->type == ARRAY) {
        for (size_t i = 0; i < data->value.dataArray.length; i++) {
            freeData(data->value.dataArray.items[i]);
        }
        free(data->value.dataArray.items);
    }
    free(data);
}
