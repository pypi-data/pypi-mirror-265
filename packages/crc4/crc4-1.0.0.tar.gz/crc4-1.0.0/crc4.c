#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <unistd.h>

static PyObject *rc4(PyObject *self, PyObject *args) {
    /* parse arguments */

    Py_buffer data, key;

    if (!PyArg_ParseTuple(args, "y*y*", &data, &key))
        return NULL;

    /* create create output object */

    PyObject *out = PyBytes_FromStringAndSize(NULL, data.len);
    if (out == NULL)
        return NULL;

    /* allocate variables */

    size_t idx, jdx, kdx;
    unsigned char S[256], temp;

    /* fill up the S buffer */

    for (idx = 0; idx < 256; idx++)
        S[idx] = idx;

    /* RC4 algorithm */

    jdx = 0;
    for (idx = 0; idx < 256; idx++) {
        jdx  = (jdx + S[idx] + ((unsigned char *)key.buf)[idx % key.len]) % 256;
        temp = S[idx];
        S[idx] = S[jdx];
        S[jdx] = temp;
    }

    idx = jdx = 0;
    for (kdx = 0; kdx < data.len; kdx++) {
        idx    = (idx + 1) % 256;
        jdx    = (jdx + S[idx]) % 256;
        temp   = S[idx];
        S[idx] = S[jdx];
        S[jdx] = temp;

        unsigned x =
            ((unsigned char *)data.buf)[kdx] ^ S[(S[idx] + S[jdx]) % 256];
        ((unsigned char *)PyBytes_AS_STRING(out))[kdx] = x;
    }

    /* :tada: */

    return out;
}

static PyMethodDef methods[] = {
    {"rc4", rc4, METH_VARARGS, "Encrypt/Decrypt using RC4 crypto."},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT, "crc4",
    "RC4 encryption/decryption in C.\n"
    "Pass in encrypted data as data with the same key to decrypt.",
    -1, methods};

PyMODINIT_FUNC PyInit_crc4(void) { return PyModule_Create(&module); }
