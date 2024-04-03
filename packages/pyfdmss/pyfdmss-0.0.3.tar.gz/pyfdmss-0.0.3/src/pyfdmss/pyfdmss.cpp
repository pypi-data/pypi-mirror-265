#include <Python.h>
#include <iostream>
#include "stdafx.h"
#include "EnvCaseGenerator.h"
#include "Codegen.h"
#include "PbcOverdozenMicroperm.h"
#include "MouseFuncX.h"
#include "MouseFuncY.h"
#include "MouseFuncZ.h"
#include "OverdozenPermsolver.h"
#include "tinyxml.h"

typedef unsigned jobIdType;

static char module_docstring[] = "todo";
static char run_docstring[] = "todo";

void SolveImpl(CmdLineParameters *io_filenames)
{
	OverdozenPermsolver ps;
	ps.SetCmdLineParameters(io_filenames);

	float vel(0.0), squareFactor(0.0), permeability(0.0), error(0.0), limit_triggered(1.0);

	if (ps.ReadFailo(io_filenames->configFileName, io_filenames->imageFileName) == true)
	{
		printf("File loaded successfully\n");
		limit_triggered = 0.0;
		vel = ps.launch();
		squareFactor = ps.GetSquareFactor();
		permeability = ps.GetPermeability();
		error = ps.GetAugeCriterionError();
	}

	TiXmlDocument doc;
	TiXmlDeclaration *decl = new TiXmlDeclaration("1.0", "", "");
	doc.LinkEndChild(decl);
	TiXmlElement *rootElem = new TiXmlElement("OverdozenPermsolverOutput");

	TiXmlElement *iLimiterTriggered = new TiXmlElement("LimiterTriggered");
	iLimiterTriggered->SetDoubleAttribute("value", limit_triggered);
	TiXmlElement *iPermeabilityM2 = new TiXmlElement("Permeability_micrometer2");
	iPermeabilityM2->SetDoubleAttribute("value", permeability);
	TiXmlElement *iPermeabilityMD = new TiXmlElement("Permeability_mD");
	iPermeabilityMD->SetDoubleAttribute("value", permeability * OverdozenPermsolver::MILLIDARCY_CONVERT_RATE);
	TiXmlElement *iAverageVelocity = new TiXmlElement("AverageVelocity");
	iAverageVelocity->SetDoubleAttribute("value", vel);
	TiXmlElement *iRelativeError = new TiXmlElement("RelativeError");
	iRelativeError->SetDoubleAttribute("value", error);
	rootElem->LinkEndChild(iAverageVelocity);
	rootElem->LinkEndChild(iPermeabilityM2);
	rootElem->LinkEndChild(iPermeabilityMD);
	rootElem->LinkEndChild(iRelativeError);
	rootElem->LinkEndChild(iLimiterTriggered);

	printf("Average velocity, micrometers/sec = %.6f\n", vel);
	printf("Average velocity within pore space, micrometers/sec = %.6f\n", vel * squareFactor);
	printf("Permeability, sq micrometers = %.6f\n", permeability);
	printf("Permeability, mD = %.6f\n", permeability * OverdozenPermsolver::MILLIDARCY_CONVERT_RATE);
	printf("Open pore space fraction at inlet = %.6f\n", 1.0 / squareFactor);
	printf("Relative error = %.6f\n", error);

	const char *output_fnames[] = {
		io_filenames->velXFileName,
		io_filenames->velYFileName,
		io_filenames->velZFileName,
		io_filenames->pressuresFileName,
		io_filenames->fullVelsFileName};

	ps.printVelPrsFieldsCustom(output_fnames);

	doc.LinkEndChild(rootElem);
	doc.SaveFile(io_filenames->summaryFileName);
}



static void run(PyObject *self, PyObject *args, PyObject *keywds) {
  const char * config_path = "";
  const char * image_path = "";
  const char * summary_path = "";
  const char * velx_path = "";
  const char * vely_path = "";
  const char * velz_path = "";
  const char * pressure_path = "";
  const char * full_vel_path = "";
  const char * comp_vel_path = "";
  const char * log_path = "";
  
  static char *kwlist[] = {"config_path",
        "image_path",
        "summary_path",
        "velx_path",
        "vely_path",
        "velz_path",
        "pressure_path",
        "full_vel_path",
        "comp_vel_path",
        "log_path", NULL};
  if (!PyArg_ParseTupleAndKeywords(
          args, keywds, "ssssssssss", kwlist, &config_path,
          &image_path, &summary_path, &velx_path, &vely_path, 
          &velz_path, &pressure_path, &full_vel_path, &comp_vel_path, &log_path)){
    return;
  }

  CmdLineParameters io_filenames (
      config_path,
      image_path,
      summary_path,
      velx_path,
      vely_path,
      velz_path,
      pressure_path,
      full_vel_path,
      comp_vel_path,
      log_path);

  SolveImpl(&io_filenames);
  return;
}

static PyMethodDef module_methods[] = {
    {"run", (PyCFunction)run, METH_VARARGS | METH_KEYWORDS,
     run_docstring},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef moduledef = {PyModuleDef_HEAD_INIT, "pyfdmss",
                                       module_docstring, -1, module_methods};

PyMODINIT_FUNC PyInit_pyfdmss(void) {
  Py_Initialize();
  PyObject *module = PyModule_Create(&moduledef);
  if (!module) {
    return NULL;
  }
  return module;
}