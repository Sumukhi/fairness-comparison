import sys
sys.path.append('/home/h205c/Derek/fairness-comparison')
from algorithms.AbstractAlgorithm import *
from algorithms.zafar.zafar_classifier import *
import algorithms.zafar.fair_classification.utils as ut
import algorithms.zafar.fair_classification.loss_funcs as lf
from datetime import datetime

class ZafarAlgorithm(AbstractAlgorithm):
  def __init__(self, *args, **kwargs):
    super(ZafarAlgorithm, self).__init__(*args, **kwargs)

  def run(self):
    startTime = datetime.now()
    sensitive_attrs = [str(self.sensitive_attr)]
    loss_function = lf._logistic_loss

    # Defaults to None
    if "gamma" in list(self.params.keys()):
      gamma = self.params["gamma"]
    else:
      gamma = None

    # Defaults to 0
    if "apply_accuracy_constraint" in list(self.params.keys()):
      apply_accuracy_constraint = self.params["apply_accuracy_constraint"]
    else:
      apply_accuracy_constraint = 0  

    # Defaults to 0
    if "apply_fairness_constraints" in list(self.params.keys()):
      apply_fairness_constraints = self.params["apply_fairness_constraints"]
    else:
      apply_fairness_constraints = 0

    # Defaults to 0
    if "sep_constraint" in list(self.params.keys()):
      sep_constraint = self.params["sep_constraint"]
    else:
      sep_constraint = 0 

    # Defaults to {}
    if "sensitive_attrs_to_cov_thresh" in list(self.params.keys()):
      sensitive_attrs_to_cov_thresh = self.params["sensitive_attrs_to_cov_thresh"]
      '''
      f = open("compare.txt","w")
      for y in self.y_train:
        f.write(str(y) + ", ")
      f.write("END OF Y_TRAIN\n")
      for z in self.x_control_train[sensitive_attrs[0]]:
        f.write(str(z) + ", ")
      f.write("END OF CONTROL")
      f.close()
      '''
    else:
      sensitive_attrs_to_cov_thresh = {}

    w = ut.train_model(self.x_train, self.y_train, self.x_control_train, loss_function, apply_fairness_constraints, apply_accuracy_constraint, sep_constraint, sensitive_attrs, sensitive_attrs_to_cov_thresh, gamma)
    distances_boundary_test = (np.dot(self.x_test, w)).tolist()
    predictions = np.sign(distances_boundary_test)

    fixed_y_test = []
    fixed_predictions = []

    for x in self.y_test:
      if x == -1:
        fixed_y_test.append(0)
      elif x == 1:
        fixed_y_test.append(1)
      elif x == 0:
        fixed_y_test.append(0)
      else:
        print("Incorrect value in class values")

    for x in predictions:
      if x == -1:
        fixed_predictions.append(0)
      elif x == 1:
        fixed_predictions.append(1)
      elif x == 0:
        fixed_predictions.append(0)
      else:
        print("Incorrect value in class values")

    zafar_actual, zafar_predicted, zafar_protected = fixed_y_test, fixed_predictions, self.x_control_test[self.sensitive_attr]
    zafar_time = datetime.now() - startTime

    return zafar_actual, zafar_predicted, zafar_protected, zafar_time

def test():

  loss_function = lf._logistic_loss
  x_train = [[1,0,1,0,0],[1,1,0,1,0],[1,0,0,1,1],[0,1,0,0,0],[0,1,0,0,1]]
  x_control = [0,1,0,1,0]
  y_train = [1,0,0,1,0]
  
  w = ut.train_model(x_train, y_train, x_control, loss_function, 0, 1, 1, 'race', {}, 1000.0)
  distances_boundary_test = (np.dot(self.x_test, w)).tolist()
  predictions = np.sign(distances_boundary_test)

  fixed_y_test = []
  fixed_predictions = []

  for x in self.y_test:
    if x == -1:
      fixed_y_test.append(0)
    elif x == 1:
      fixed_y_test.append(1)
    elif x == 0:
      fixed_y_test.append(0)
    else:
      print("Incorrect value in class values")

  for x in predictions:
    if x == -1:
      fixed_predictions.append(0)
    elif x == 1:
      fixed_predictions.append(1)
    elif x == 0:
      fixed_predictions.append(0)
    else:
      print("Incorrect value in class values")

  
if __name__ == "__main__":
  test()