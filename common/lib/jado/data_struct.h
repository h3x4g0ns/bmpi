#include <stdlib.h>
#include <string.h>

typedef enum {
    INTEGER,
    STRING,
    NESTED,
    ARRAY
} DataType;

typedef struct Data;

typedef struct {
    struct Data** items;
    size_t length;
} DataArray;

struct Data {
    DataType type;
    union {
        int intValue;
        char *stringValue;
        struct Data *nestedData;
        DataArray dataArray;
    } value;
};

struct Data *createIntData(int value);
struct Data *createStringData(char *value);
struct Data *createNestedData(struct Data *nested);
struct Data *createArrayData(struct Data** items, size_t length);
void printData(struct Data *data);
void freeData(struct Data *data);
