#ifdef __cplusplus
extern "C" {
#endif

typedef void* JADO;  // Opaque pointer to JADO instance

// Exposed C functions
JADO JADO_new();
void JADO_set(JADO j, const char* key, const char* value);
const char* JADO_get(JADO j, const char* key);
void JADO_delete(JADO j);

#ifdef __cplusplus
}
#endif
