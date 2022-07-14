{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<p style=\"text-align:center\">\n",
    "    <a href=\"https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork26802033-2022-01-01\" target=\"_blank\">\n",
    "    <img src=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png\" width=\"200\" alt=\"Skills Network Logo\"  />\n",
    "    </a>\n",
    "</p>\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# **Space X  Falcon 9 First Stage Landing Prediction**\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Assignment:  Machine Learning Prediction\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Estimated time needed: **60** minutes\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Space X advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is because Space X can reuse the first stage. Therefore if we can determine if the first stage will land, we can determine the cost of a launch. This information can be used if an alternate company wants to bid against space X for a rocket launch.   In this lab, you will create a machine learning pipeline  to predict if the first stage will land given the data from the preceding labs.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/landing\\_1.gif)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Several examples of an unsuccessful landing are shown here:\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/crash.gif)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Most unsuccessful landings are planed. Space X; performs a controlled landing in the oceans.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Objectives\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Perform exploratory  Data Analysis and determine Training Labels\n",
    "\n",
    "*   create a column for the class\n",
    "*   Standardize the data\n",
    "*   Split into training data and test data\n",
    "\n",
    "\\-Find best Hyperparameter for SVM, Classification Trees and Logistic Regression\n",
    "\n",
    "*   Find the method performs best using test data\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "***\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Import Libraries and Define Auxiliary Functions\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We will import the following libraries for the lab\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "collapsed": true,
    "jupyter": {
     "outputs_hidden": true
    },
    "tags": []
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
    }
   ],
   "source": [
    "# Pandas is a software library written for the Python programming language for data manipulation and analysis.\n",
    "import pandas as pd\n",
    "# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays\n",
    "import numpy as np\n",
    "# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.\n",
    "import matplotlib.pyplot as plt\n",
    "#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics\n",
    "import seaborn as sns\n",
    "# Preprocessing allows us to standarsize our data\n",
    "from sklearn import preprocessing\n",
    "# Allows us to split our data into training and testing data\n",
    "from sklearn.model_selection import train_test_split\n",
    "# Allows us to test parameters of classification algorithms and find the best one\n",
    "from sklearn.model_selection import GridSearchCV\n",
    "# Logistic Regression classification algorithm\n",
    "from sklearn.linear_model import LogisticRegression\n",
    "# Support Vector Machine classification algorithm\n",
    "from sklearn.svm import SVC\n",
    "# Decision Tree classification algorithm\n",
    "from sklearn.tree import DecisionTreeClassifier\n",
    "# K Nearest Neighbors classification algorithm\n",
    "from sklearn.neighbors import KNeighborsClassifier"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This function is to plot the confusion matrix.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "def plot_confusion_matrix(y,y_predict):\n",
    "    \"this function plots the confusion matrix\"\n",
    "    from sklearn.metrics import confusion_matrix\n",
    "\n",
    "    cm = confusion_matrix(y, y_predict)\n",
    "    ax= plt.subplot()\n",
    "    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells\n",
    "    ax.set_xlabel('Predicted labels')\n",
    "    ax.set_ylabel('True labels')\n",
    "    ax.set_title('Confusion Matrix'); \n",
    "    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed'])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Load the dataframe\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Load the data\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>FlightNumber</th>\n",
       "      <th>Date</th>\n",
       "      <th>BoosterVersion</th>\n",
       "      <th>PayloadMass</th>\n",
       "      <th>Orbit</th>\n",
       "      <th>LaunchSite</th>\n",
       "      <th>Outcome</th>\n",
       "      <th>Flights</th>\n",
       "      <th>GridFins</th>\n",
       "      <th>Reused</th>\n",
       "      <th>Legs</th>\n",
       "      <th>LandingPad</th>\n",
       "      <th>Block</th>\n",
       "      <th>ReusedCount</th>\n",
       "      <th>Serial</th>\n",
       "      <th>Longitude</th>\n",
       "      <th>Latitude</th>\n",
       "      <th>Class</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "      <td>2010-06-04</td>\n",
       "      <td>Falcon 9</td>\n",
       "      <td>6104.959412</td>\n",
       "      <td>LEO</td>\n",
       "      <td>CCAFS SLC 40</td>\n",
       "      <td>None None</td>\n",
       "      <td>1</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>NaN</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0</td>\n",
       "      <td>B0003</td>\n",
       "      <td>-80.577366</td>\n",
       "      <td>28.561857</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2</td>\n",
       "      <td>2012-05-22</td>\n",
       "      <td>Falcon 9</td>\n",
       "      <td>525.000000</td>\n",
       "      <td>LEO</td>\n",
       "      <td>CCAFS SLC 40</td>\n",
       "      <td>None None</td>\n",
       "      <td>1</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>NaN</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0</td>\n",
       "      <td>B0005</td>\n",
       "      <td>-80.577366</td>\n",
       "      <td>28.561857</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>3</td>\n",
       "      <td>2013-03-01</td>\n",
       "      <td>Falcon 9</td>\n",
       "      <td>677.000000</td>\n",
       "      <td>ISS</td>\n",
       "      <td>CCAFS SLC 40</td>\n",
       "      <td>None None</td>\n",
       "      <td>1</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>NaN</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0</td>\n",
       "      <td>B0007</td>\n",
       "      <td>-80.577366</td>\n",
       "      <td>28.561857</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>4</td>\n",
       "      <td>2013-09-29</td>\n",
       "      <td>Falcon 9</td>\n",
       "      <td>500.000000</td>\n",
       "      <td>PO</td>\n",
       "      <td>VAFB SLC 4E</td>\n",
       "      <td>False Ocean</td>\n",
       "      <td>1</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>NaN</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0</td>\n",
       "      <td>B1003</td>\n",
       "      <td>-120.610829</td>\n",
       "      <td>34.632093</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5</td>\n",
       "      <td>2013-12-03</td>\n",
       "      <td>Falcon 9</td>\n",
       "      <td>3170.000000</td>\n",
       "      <td>GTO</td>\n",
       "      <td>CCAFS SLC 40</td>\n",
       "      <td>None None</td>\n",
       "      <td>1</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>NaN</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0</td>\n",
       "      <td>B1004</td>\n",
       "      <td>-80.577366</td>\n",
       "      <td>28.561857</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   FlightNumber        Date BoosterVersion  PayloadMass Orbit    LaunchSite  \\\n",
       "0             1  2010-06-04       Falcon 9  6104.959412   LEO  CCAFS SLC 40   \n",
       "1             2  2012-05-22       Falcon 9   525.000000   LEO  CCAFS SLC 40   \n",
       "2             3  2013-03-01       Falcon 9   677.000000   ISS  CCAFS SLC 40   \n",
       "3             4  2013-09-29       Falcon 9   500.000000    PO   VAFB SLC 4E   \n",
       "4             5  2013-12-03       Falcon 9  3170.000000   GTO  CCAFS SLC 40   \n",
       "\n",
       "       Outcome  Flights  GridFins  Reused   Legs LandingPad  Block  \\\n",
       "0    None None        1     False   False  False        NaN    1.0   \n",
       "1    None None        1     False   False  False        NaN    1.0   \n",
       "2    None None        1     False   False  False        NaN    1.0   \n",
       "3  False Ocean        1     False   False  False        NaN    1.0   \n",
       "4    None None        1     False   False  False        NaN    1.0   \n",
       "\n",
       "   ReusedCount Serial   Longitude   Latitude  Class  \n",
       "0            0  B0003  -80.577366  28.561857      0  \n",
       "1            0  B0005  -80.577366  28.561857      0  \n",
       "2            0  B0007  -80.577366  28.561857      0  \n",
       "3            0  B1003 -120.610829  34.632093      0  \n",
       "4            0  B1004  -80.577366  28.561857      0  "
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data = pd.read_csv(\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv\")\n",
    "\n",
    "# If you were unable to complete the previous lab correctly you can uncomment and load this csv\n",
    "\n",
    "# data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/dataset_part_2.csv')\n",
    "\n",
    "data.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>FlightNumber</th>\n",
       "      <th>PayloadMass</th>\n",
       "      <th>Flights</th>\n",
       "      <th>Block</th>\n",
       "      <th>ReusedCount</th>\n",
       "      <th>Orbit_ES-L1</th>\n",
       "      <th>Orbit_GEO</th>\n",
       "      <th>Orbit_GTO</th>\n",
       "      <th>Orbit_HEO</th>\n",
       "      <th>Orbit_ISS</th>\n",
       "      <th>...</th>\n",
       "      <th>Serial_B1058</th>\n",
       "      <th>Serial_B1059</th>\n",
       "      <th>Serial_B1060</th>\n",
       "      <th>Serial_B1062</th>\n",
       "      <th>GridFins_False</th>\n",
       "      <th>GridFins_True</th>\n",
       "      <th>Reused_False</th>\n",
       "      <th>Reused_True</th>\n",
       "      <th>Legs_False</th>\n",
       "      <th>Legs_True</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1.0</td>\n",
       "      <td>6104.959412</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2.0</td>\n",
       "      <td>525.000000</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>3.0</td>\n",
       "      <td>677.000000</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>4.0</td>\n",
       "      <td>500.000000</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5.0</td>\n",
       "      <td>3170.000000</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>85</th>\n",
       "      <td>86.0</td>\n",
       "      <td>15400.000000</td>\n",
       "      <td>2.0</td>\n",
       "      <td>5.0</td>\n",
       "      <td>2.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>86</th>\n",
       "      <td>87.0</td>\n",
       "      <td>15400.000000</td>\n",
       "      <td>3.0</td>\n",
       "      <td>5.0</td>\n",
       "      <td>2.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>87</th>\n",
       "      <td>88.0</td>\n",
       "      <td>15400.000000</td>\n",
       "      <td>6.0</td>\n",
       "      <td>5.0</td>\n",
       "      <td>5.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>88</th>\n",
       "      <td>89.0</td>\n",
       "      <td>15400.000000</td>\n",
       "      <td>3.0</td>\n",
       "      <td>5.0</td>\n",
       "      <td>2.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>89</th>\n",
       "      <td>90.0</td>\n",
       "      <td>3681.000000</td>\n",
       "      <td>1.0</td>\n",
       "      <td>5.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>90 rows × 83 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "    FlightNumber   PayloadMass  Flights  Block  ReusedCount  Orbit_ES-L1  \\\n",
       "0            1.0   6104.959412      1.0    1.0          0.0          0.0   \n",
       "1            2.0    525.000000      1.0    1.0          0.0          0.0   \n",
       "2            3.0    677.000000      1.0    1.0          0.0          0.0   \n",
       "3            4.0    500.000000      1.0    1.0          0.0          0.0   \n",
       "4            5.0   3170.000000      1.0    1.0          0.0          0.0   \n",
       "..           ...           ...      ...    ...          ...          ...   \n",
       "85          86.0  15400.000000      2.0    5.0          2.0          0.0   \n",
       "86          87.0  15400.000000      3.0    5.0          2.0          0.0   \n",
       "87          88.0  15400.000000      6.0    5.0          5.0          0.0   \n",
       "88          89.0  15400.000000      3.0    5.0          2.0          0.0   \n",
       "89          90.0   3681.000000      1.0    5.0          0.0          0.0   \n",
       "\n",
       "    Orbit_GEO  Orbit_GTO  Orbit_HEO  Orbit_ISS  ...  Serial_B1058  \\\n",
       "0         0.0        0.0        0.0        0.0  ...           0.0   \n",
       "1         0.0        0.0        0.0        0.0  ...           0.0   \n",
       "2         0.0        0.0        0.0        1.0  ...           0.0   \n",
       "3         0.0        0.0        0.0        0.0  ...           0.0   \n",
       "4         0.0        1.0        0.0        0.0  ...           0.0   \n",
       "..        ...        ...        ...        ...  ...           ...   \n",
       "85        0.0        0.0        0.0        0.0  ...           0.0   \n",
       "86        0.0        0.0        0.0        0.0  ...           1.0   \n",
       "87        0.0        0.0        0.0        0.0  ...           0.0   \n",
       "88        0.0        0.0        0.0        0.0  ...           0.0   \n",
       "89        0.0        0.0        0.0        0.0  ...           0.0   \n",
       "\n",
       "    Serial_B1059  Serial_B1060  Serial_B1062  GridFins_False  GridFins_True  \\\n",
       "0            0.0           0.0           0.0             1.0            0.0   \n",
       "1            0.0           0.0           0.0             1.0            0.0   \n",
       "2            0.0           0.0           0.0             1.0            0.0   \n",
       "3            0.0           0.0           0.0             1.0            0.0   \n",
       "4            0.0           0.0           0.0             1.0            0.0   \n",
       "..           ...           ...           ...             ...            ...   \n",
       "85           0.0           1.0           0.0             0.0            1.0   \n",
       "86           0.0           0.0           0.0             0.0            1.0   \n",
       "87           0.0           0.0           0.0             0.0            1.0   \n",
       "88           0.0           1.0           0.0             0.0            1.0   \n",
       "89           0.0           0.0           1.0             0.0            1.0   \n",
       "\n",
       "    Reused_False  Reused_True  Legs_False  Legs_True  \n",
       "0            1.0          0.0         1.0        0.0  \n",
       "1            1.0          0.0         1.0        0.0  \n",
       "2            1.0          0.0         1.0        0.0  \n",
       "3            1.0          0.0         1.0        0.0  \n",
       "4            1.0          0.0         1.0        0.0  \n",
       "..           ...          ...         ...        ...  \n",
       "85           0.0          1.0         0.0        1.0  \n",
       "86           0.0          1.0         0.0        1.0  \n",
       "87           0.0          1.0         0.0        1.0  \n",
       "88           0.0          1.0         0.0        1.0  \n",
       "89           1.0          0.0         0.0        1.0  \n",
       "\n",
       "[90 rows x 83 columns]"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "X = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv')\n",
    "\n",
    "# If you were unable to complete the previous lab correctly you can uncomment and load this csv\n",
    "\n",
    "# X = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/dataset_part_3.csv')\n",
    "\n",
    "X.head(100)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  1\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Create a NumPy array from the column <code>Class</code> in <code>data</code>, by applying the method <code>to_numpy()</code>  then\n",
    "assign it  to the variable <code>Y</code>,make sure the output is a  Pandas series (only one bracket df\\['name of  column']).\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "y= data['Class'].to_numpy()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  2\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Standardize the data in <code>X</code> then reassign it to the variable  <code>X</code> using the transform provided below.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "# students get this \n",
    "transform = preprocessing.StandardScaler()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "X = transform.fit_transform(X)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We split the data into training and testing data using the  function  <code>train_test_split</code>.   The training data is divided into validation data, a second set used for training  data; then the models are trained and hyperparameters are selected using the function <code>GridSearchCV</code>.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  3\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Use the function train_test_split to split the data X and Y into training and test data. Set the parameter test_size to  0.2 and random_state to 2. The training data and test data should be assigned to the following labels.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<code>X_train, X_test, Y_train, Y_test</code>\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, random_state=4)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "we can see we only have 18 test samples.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(18,)"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "Y_test.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  4\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Create a logistic regression object  then create a  GridSearchCV object  <code>logreg_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "parameters ={'C':[0.01,0.1,1],\n",
    "             'penalty':['l2'],\n",
    "             'solver':['lbfgs']}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {
    "collapsed": true,
    "jupyter": {
     "outputs_hidden": true
    },
    "tags": []
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
   ],
   "source": [
    "parameters ={\"C\":[0.01,0.1,1],'penalty':['l2'], 'solver':['lbfgs']}# l1 lasso l2 ridge\n",
    "lr=LogisticRegression()\n",
    "logreg_cv = GridSearchCV(lr, parameters, scoring='accuracy', cv=10)\n",
    "logreg_cv = logreg_cv.fit(X_train, Y_train)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We output the <code>GridSearchCV</code> object for logistic regression. We display the best parameters using the data attribute <code>best_params\\_</code> and the accuracy on the validation data using the data attribute <code>best_score\\_</code>.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "tuned hpyerparameters :(best parameters)  {'C': 0.01, 'penalty': 'l2', 'solver': 'lbfgs'}\n",
      "accuracy : 0.8333333333333334\n"
     ]
    }
   ],
   "source": [
    "print(\"tuned hpyerparameters :(best parameters) \",logreg_cv.best_params_)\n",
    "print(\"accuracy :\",logreg_cv.best_score_)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  5\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Calculate the accuracy on the test data using the method <code>score</code>:\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {
    "collapsed": true,
    "jupyter": {
     "outputs_hidden": true
    },
    "tags": []
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/home/jupyterlab/conda/envs/python/lib/python3.7/site-packages/sklearn/linear_model/base.py:283: DeprecationWarning: `np.int` is a deprecated alias for the builtin `int`. To silence this warning, use `int` by itself. Doing this will not modify any behavior and is safe. When replacing `np.int`, you may wish to use e.g. `np.int64` or `np.int32` to specify the precision. If you wish to review your current use, check the release note link for additional information.\n",
      "Deprecated in NumPy 1.20; for more details and guidance: https://numpy.org/devdocs/release/1.20.0-notes.html#deprecations\n",
      "  indices = (scores > 0).astype(np.int)\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "0.7222222222222222"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "lr_accuracy = logreg_cv.score(X_test, Y_test)\n",
    "lr_accuracy"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Lets look at the confusion matrix:\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/home/jupyterlab/conda/envs/python/lib/python3.7/site-packages/sklearn/linear_model/base.py:283: DeprecationWarning: `np.int` is a deprecated alias for the builtin `int`. To silence this warning, use `int` by itself. Doing this will not modify any behavior and is safe. When replacing `np.int`, you may wish to use e.g. `np.int64` or `np.int32` to specify the precision. If you wish to review your current use, check the release note link for additional information.\n",
      "Deprecated in NumPy 1.20; for more details and guidance: https://numpy.org/devdocs/release/1.20.0-notes.html#deprecations\n",
      "  indices = (scores > 0).astype(np.int)\n"
     ]
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "yhat=logreg_cv.predict(X_test)\n",
    "plot_confusion_matrix(Y_test,yhat)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Examining the confusion matrix, we see that logistic regression can distinguish between the different classes.  We see that the major problem is false positives.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  6\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Create a support vector machine object then  create a  <code>GridSearchCV</code> object  <code>svm_cv</code> with cv - 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [],
   "source": [
    "parameters = {'kernel':('linear', 'rbf','poly','rbf', 'sigmoid'),\n",
    "              'C': np.logspace(-3, 3, 5),\n",
    "              'gamma':np.logspace(-3, 3, 5)}\n",
    "svm = SVC()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {
    "collapsed": true,
    "jupyter": {
     "outputs_hidden": true
    },
    "tags": []
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
    }
   ],
   "source": [
    "svm_cv = GridSearchCV(svm, parameters, scoring='accuracy', cv=10)\n",
    "svm_cv = svm_cv.fit(X_train, Y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "tuned hpyerparameters :(best parameters)  {'C': 1.0, 'gamma': 0.03162277660168379, 'kernel': 'sigmoid'}\n",
      "accuracy : 0.8611111111111112\n"
     ]
    }
   ],
   "source": [
    "print(\"tuned hpyerparameters :(best parameters) \",svm_cv.best_params_)\n",
    "print(\"accuracy :\",svm_cv.best_score_)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  7\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Calculate the accuracy on the test data using the method <code>score</code>:\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.7777777777777778"
      ]
     },
     "execution_count": 21,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "svm_accuracy = svm_cv.score(X_test, Y_test)\n",
    "svm_accuracy"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We can plot the confusion matrix\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "yhat=svm_cv.predict(X_test)\n",
    "plot_confusion_matrix(Y_test,yhat)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  8\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Create a decision tree classifier object then  create a  <code>GridSearchCV</code> object  <code>tree_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [],
   "source": [
    "parameters = {'criterion': ['gini', 'entropy'],\n",
    "     'splitter': ['best', 'random'],\n",
    "     'max_depth': [2*n for n in range(1,10)],\n",
    "     'max_features': ['auto', 'sqrt'],\n",
    "     'min_samples_leaf': [1, 2, 4],\n",
    "     'min_samples_split': [2, 5, 10]}\n",
    "\n",
    "tree = DecisionTreeClassifier()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {
    "collapsed": true,
    "jupyter": {
     "outputs_hidden": true
    },
    "tags": []
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
    }
   ],
   "source": [
    "tree_cv = GridSearchCV(tree, parameters, scoring='accuracy', cv=10)\n",
    "tree_cv = tree_cv.fit(X_train, Y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "tuned hpyerparameters :(best parameters)  {'criterion': 'gini', 'max_depth': 4, 'max_features': 'auto', 'min_samples_leaf': 1, 'min_samples_split': 5, 'splitter': 'best'}\n",
      "accuracy : 0.9166666666666666\n"
     ]
    }
   ],
   "source": [
    "print(\"tuned hpyerparameters :(best parameters) \",tree_cv.best_params_)\n",
    "print(\"accuracy :\",tree_cv.best_score_)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  9\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Calculate the accuracy of tree_cv on the test data using the method <code>score</code>:\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.7777777777777778"
      ]
     },
     "execution_count": 27,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "tree_cv_accuracy = tree_cv.score(X_test, Y_test)\n",
    "tree_cv_accuracy"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We can plot the confusion matrix\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAWgAAAEWCAYAAABLzQ1kAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjUuMiwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8qNh9FAAAACXBIWXMAAAsTAAALEwEAmpwYAAAfFUlEQVR4nO3dd5xdVbnG8d+TAgRIAoHQApiggApKREC6oSi9iVdAsCAYuNJULIAICtZ7lQvei3ojqJiEKCBFOlIi5aKmEGqQKKGERAiBFHoy894/9h5yMs6cNmefsybzfPnsz5yzy1pvZg7vrFl7rbUVEZiZWXr6tToAMzPrmhO0mVminKDNzBLlBG1mlignaDOzRDlBm5klygnaekzSIEnXS1ok6coelHO0pNsaGVsrSLpZ0mdaHYf1fk7QfYikT0qaKukVSfPyRLJrA4r+OLA+sE5E/Fu9hUTExIj4aAPiWYGkMZJC0tWd9m+T759cZTnfkjSh0nkRsV9EXFZnuGZvc4LuIyR9GbgQ+B5ZMt0U+ClwSAOKfwfwREQsa0BZRZkP7CxpnZJ9nwGeaFQFyvj/KWsYf5j6AElDgfOAkyLi6oh4NSKWRsT1EfHV/JxVJV0oaW6+XShp1fzYGElzJJ0u6YW89X1sfuzbwDnAEXnL/LjOLU1JI/OW6oD8/WclPSlpiaTZko4u2X9vyXU7S5qSd51MkbRzybHJks6XdF9ezm2S1i3zbXgLuBY4Mr++P/AJYGKn79VFkp6VtFjSNEm75fv3Bc4q+Xc+WBLHdyXdB7wGbJbvOz4//jNJV5WU/0NJd0hStT8/67ucoPuGnYDVgGvKnPMNYEdgNLANsANwdsnxDYChwAjgOOBiSWtHxLlkrfLfRcSaEXFpuUAkrQH8BNgvIgYDOwMzujhvGHBjfu46wAXAjZ1awJ8EjgXWA1YBvlKubuA3wKfz1/sAjwJzO50zhex7MAy4HLhS0moRcUunf+c2Jdd8ChgLDAae7lTe6cD7818+u5F97z4TXmPBquAE3TesA7xYoQviaOC8iHghIuYD3yZLPB2W5seXRsRNwCvAlnXG0w5sLWlQRMyLiEe7OOcAYFZEjI+IZRExCXgcOKjknF9FxBMR8TpwBVli7VZE/B8wTNKWZIn6N12cMyEiFuR1/hhYlcr/zl9HxKP5NUs7lfcacAzZL5gJwCkRMadCeWaAE3RfsQBYt6OLoRsbsWLr7+l839tldErwrwFr1hpIRLwKHAGcCMyTdKOkd1cRT0dMI0re/7OOeMYDJwN70MVfFHk3zsy8W2Uh2V8N5bpOAJ4tdzAi/go8CYjsF4lZVZyg+4b7gTeAQ8ucM5fsZl+HTfnXP/+r9Sqwesn7DUoPRsStEfERYEOyVvEvqoinI6bn6oypw3jgC8BNeev2bXkXxNfJ+qbXjoi1gEVkiRWgu26Jst0Vkk4ia4nPBb5Wd+TW5zhB9wERsYjsRt7Fkg6VtLqkgZL2k/Qf+WmTgLMlDc9vtp1D9id5PWYAu0vaNL9BeWbHAUnrSzo474t+k6yrpK2LMm4CtsiHBg6QdATwXuCGOmMCICJmAx8m63PvbDCwjGzExwBJ5wBDSo4/D4ysZaSGpC2A75B1c3wK+Jqk0fVFb32NE3QfEREXAF8mu/E3n+zP8pPJRjZAlkSmAg8BDwPT83311PVH4Hd5WdNYMan2I7txNhd4iSxZfqGLMhYAB+bnLiBreR4YES/WE1Onsu+NiK7+OrgVuJls6N3TZH91lHZfdEzCWSBpeqV68i6lCcAPI+LBiJhFNhJkfMcIGbNy5JvJZmZpcgvazCxRTtBmZg0m6Zf5pK5HSvYNk/RHSbPyr2tXKscJ2sys8X4N7Ntp3xnAHRGxOXBH/r4s90GbmRVA0kjghojYOn//N2BMRMyTtCEwOSLKToIqN3GhpX4z4hj/5jCzqnz6uQk9Xttk6YtPVp1zVhn+zhPIpvd3GBcR4ypctn5EzAPIk/R6lepJNkGbmTVVe1fD8buWJ+NKCbnHnKDNzACiveganpe0YUkXxwuVLvBNQjMzgPb26rf6/IFsDXLyr9dVusAtaDMzIBrYgpY0CRhDtkjZHOBc4AfAFZKOA54BKj59yAnazAygrXEPBIqIo7o5tFct5ThBm5lBTTcJm8UJ2swMmnGTsGZO0GZm0JObf4VxgjYzo7E3CRvFCdrMDNyCNjNLVtvSyuc0mRO0mRn4JqGZWbLcxWFmlii3oM3MEuUWtJlZmqLdNwnNzNLkFrSZWaLcB21mligvlmRmlii3oM3MEuU+aDOzRDVwwf5GcYI2MwO3oM3MUhXhm4RmZmlyC9rMLFEexWFmlii3oM3MEuVRHGZmiXIXh5lZotzFYWaWKCdoM7NEuYvDzCxRvkloZpYod3GYmSXKXRxmZolyC9rMLFFO0GZmiYpodQT/wgnazAxgmUdxmJmlKcGbhP1aHYCZWRLa26vfKpD0JUmPSnpE0iRJq9UTkhO0mRlkfdDVbmVIGgGcCmwXEVsD/YEj6wnJXRxmZtDoURwDgEGSlgKrA3PrKcQtaDMzqKmLQ9JYSVNLtrEdxUTEc8CPgGeAecCiiLitnpDcgjYzA6Kt+ofGRsQ4YFxXxyStDRwCjAIWAldKOiYiJtQak1vQZmbQyJuEewOzI2J+RCwFrgZ2rickt6DNzKCRw+yeAXaUtDrwOrAXMLWegpygzcwA2hszkzAi/iLpKmA6sAx4gG66QypxgjYzg4aO4oiIc4Fze1qOE7SZGUANNwmbxTcJE6d+4sBbv8Oel53e6lAsIf5cFKCBMwkbxQk6ce8+fl8WzaprjLutxPy5KEB7VL81ScMTtKQlkhZ3tzW6vpXZ6hsOY+O9RjNr0uRWh2IJ8eeiINFe/dYkDe+DjojBAJLOA/4JjAcEHA0MbnR9K7Ptv30M074ziYFrDmp1KJYQfy4K0sSWcbWK7OLYJyJ+GhFLImJxRPwMOLzcBaXTJ+96dVaBoaVvxN6jeePFxbz08FOtDsUS4s9FcaK9veqtWYocxdEm6Wjgt0AARwFlb5OWTp/8zYhj0vt11kTrbbcFG390W0bsuQ39Vx3IwMGD2PUn/869p/6s1aFZC/lzUaAER3EoCnrMi6SRwEXALmQJ+j7gixHxVDXX9/UEXWr9nd7DVifuz52f+XGrQ7GE+HOx3Kefm6CelvHqeUdXnXPWOGdij+urRmEt6DwRH1JU+WZmDdWXHhoraTjweWBkaT0R8bmi6lxZPX//TJ6/f2arw7DE+HPRYAneJCyyD/o64B7gdir0PZuZtVyCzyQsMkGvHhFfL7B8M7PG6WMt6Bsk7R8RNxVYh5lZQ8Sy9P7QLzJBnwacJelNYCnZZJWIiCEF1mlmVp++1ILumFFoZtYr9LE+6I5nc20OrNaxLyLuLrJOM7O69KUWtKTjybo5NgZmADsC9wN7FlWnmVm9IsEEXeRaHKcB2wNPR8QewAeA+QXWZ2ZWv2Vt1W9NUmQXxxsR8YYkJK0aEY9L2rLA+szM6pdgC7rIBD1H0lrAtcAfJb0MeIVxM0tTX0rQEXFY/vJbku4ChgK3FFWfmVlPFLVwXE80PEFLGtbF7ofzr2sCLzW6TjOzHusjLehpZMuLli7H1/E+gM0KqNPMrGf6QoKOiFGNLtPMrGixrI9NVDEz6zXSy89O0GZmkOZEFSdoMzNIsg+6sJmEksZXs8/MLAntNWxNUmQLeqvSN5L6Ax8ssD4zs7r1iS4OSWcCZwGDJC1m+XC7t4Bxja7PzKwRYll6CbrhXRwR8f18Lej/jIghETE439aJiDMbXZ+ZWUP0pS6OiDhT0sHA7vmuyRFxQ1H1mZn1RILr9Re6HvT3gR2Aifmu0yTt4la0mSWpLyVo4ABgdET2e0nSZcADgBO0mSUnxRZ0TX3QktaW9P4aLlmr5PXQWuoyM2umWFb9VomktSRdJelxSTMl7VRPTBVb0JImAwfn584A5kv6U0R8ucKl3wceyJcaFVlftFvPZpakBregLwJuiYiPS1oFWL2eQqrp4hgaEYvzZwz+KiLOlfRQpYsiYlKe3LcnS9Bfj4h/1hOkmVnRGpWgJQ0ha5B+FiAi3iIbZlyzaro4BkjaEPgEUOsojH7Ai8DLwBaSdq9wvplZa4Sq3iSNlTS1ZBtbUtJmZM9f/ZWkByRdImmNekKqpgV9HnArcG9ETJG0GTCr0kWSfggcATzK8vujAdxdT6BmZkWqpQUdEePofuLdAGBb4JSI+Iuki4AzgG/WGlPFBB0RVwJXlrx/Eji8irIPBbaMiDdrDcrMrNmiXZVPqs4cYE5E/CV/fxVZgq5Ztwla0n+TtXi7FBGnVij7SWAg4ARtZslrb2tMgo6If0p6VtKWEfE3YC/gsXrKKteCnlpXdMu9BsyQdAclSbqKxG5m1nQNHsVxCjAxH8HxJHBsPYV0m6Aj4rLS95LWiIhXayj7D/lmZpa8BnZxEBEzgO16Wk4146B3Ai4leyL3ppK2AU6IiC9UCPCycsfNzFIS6S1mV9UwuwuBfYAFABHxIMsXQDIzWylEu6remqWqtTgi4llphaDaignHzKw1GnWTsJGqSdDPStoZiLzD+1RgZrFhmZk1VzNbxtWqJkGfSDavfATwHNmklZO6O1nS9ZQfnndwjTGamRUuohcm6Ih4ETi6hjJ/lH/9GLABMCF/fxTwVC3BmZk1S4rLjVYzimMzshb0jmQt4/uBL+UzCv9FRPwpv+78iCi9mXi9JE/zNrMktSfYgq5mFMflwBXAhsBGZNO+J1Vx3fA8uQMgaRQwvJ4gzcyKFqGqt2appg9aETG+5P0ESSdXcd2XgMmSOlraI4ETaozPzKwpetUoDknD8pd3SToD+C1ZF8cRwI2VCo6IWyRtDrw73/W4F04ys1T1tlEc08gSckfUpa3fAM7v6iJJe0bEnZI+1unQOyUREVfXHa2ZWUFS7IMutxbHqDrL/DBwJ3BQV8UCTtBmlpxeOcwOQNLWwHuB1Tr2RcRvujo3Is7Nv9a1epOZWSukuBZHNcPszgXGkCXom4D9gHuBLhO0pLIPk42IC2qO0sysYL2qi6PEx4FtgAci4lhJ6wOXlDl/cP51S7IHxnYsOXoQftyVmSWqvZfdJOzwekS0S1qWP632BbKHInYpIr4NIOk2YNuIWJK//xYlj84yM0tJb21BT5W0FvALspEdrwB/reK6TVnxUeNvkY2Frsrn5t9V7anWh7w+955Wh2ArqV55k7BkYf6fS7oFGBIRD1VR9njgr5KuIRu9cRjgRfzNLEm9qgUtadtyxyJiermCI+K7km4Gdst3HRsRD9QXpplZsRIcxFG2Bf3jMscC2LNS4XkSL5vIzcxS0NZezdJEzVVuosoezQzEzKyVElxttLqJKmZmK7ugF/VBm5n1Je0JdkI7QZuZAe0JtqAr9oorc4ykc/L3m0raofjQzMyaJ1DVW7NUc9vyp8BOZM8UBFgCXFxYRGZmLdCGqt6apZoujg9FxLaSHgCIiJclrVJwXGZmTdVbR3EsldSffBy3pOGk+W8xM6tbikmtmi6OnwDXAOtJ+i7ZUqPfKzQqM7MmS7EPupq1OCZKmgbsRfb4q0MjYmbhkZmZNVGCq41WtWD/psBrwPWl+yLimSIDMzNrphSH2VXTB30jyx8euxowCvgbsFWBcZmZNVVbqwPoQjVdHO8rfZ+vcndCN6ebmfVK7eqdLegVRMR0SdsXEYyZWaskONO7qj7o0ofA9gO2BeYXFpGZWQukOMyumhb04JLXy8j6pH9fTDhmZq3R6FEc+fyRqcBzEXFgPWWUTdB5BWtGxFfrKdzMrLcoYAr3acBMYEi9BXQ7UUXSgIhoI+vSMDNbqbWr+q0SSRsDBwCX9CSmci3ov5Il5xmS/gBcCbzacTAiru5JxWZmKamlD1rSWGBsya5xETGu5P2FwNdYsYu4ZtX0QQ8DFpA9g7BjPHQATtBmttKoZRRHnozHdXVM0oHACxExTdKYnsRULkGvl4/geITlifnt+HpSqZlZahp4k3AX4GBJ+5NN7hsiaUJEHFNrQeUSdH9gTeiy59wJ2sxWKo0aZhcRZwJnAuQt6K/Uk5yhfIKeFxHn1VOomVlv05beRMKyCTrBcM3MilHERJWImAxMrvf6cgl6r3oLNTPrbXrVTMKIeKmZgZiZtVKKN9ZqXizJzGxl1CsX7Dcz6wt6VReHmVlf0isX7Dcz6wvcxWFmlih3cZiZJcqjOMzMEtWeYIp2gjYzwzcJzcyS5T5oM7NEeRSHmVmi3AdtZpao9NKzE7SZGeA+aDOzZLUl2IZ2gjYzwy1oM7Nk+SahmVmi0kvPTtBmZoC7OMzMkuWbhGZmiUqxD7pfqwOw8vb56BgefeRuHn/sXr721ZNaHY61yNnfu4DdDziSQ4858e19ixYv4fjTzmL/I47j+NPOYtHiJS2MsPeLGrZmcYJOWL9+/fjJRd/lwIOO4X3b7MERRxzKe96zeavDshY4dP+P8PMLvrPCvkvGX8GO243mpt9dyo7bjebSCVe0KLqVQztR9dYsTtAJ22H7D/CPfzzF7NnPsHTpUq644joOPmifVodlLbDd6PcxdMjgFfbddc/9HLLf3gAcst/e3Hn3/a0IbaXRXsPWLE7QCdtoxAY8O2fu2+/nPDePjTbaoIURWUoWvLyQ4esOA2D4usN4aeGiFkfUu0UN/zVLITcJJX2s3PGIuLqb68YCYwHUfyj9+q1RQHS9h/Sv6x9GpHcjw2xl0JdGcRyUf10P2Bm4M3+/BzAZ6DJBR8Q4YBzAgFVGpPfdarLn5sxjk403evv9xiM2ZN6851sYkaVknbXXYv6LLzF83WHMf/Elhq01tNUh9WopjoMupIsjIo6NiGPJbni+NyIOj4jDga2KqG9lNWXqDN71rlGMHLkJAwcO5BOfOITrb7it1WFZIsbsuiPX3Xw7ANfdfDt77LZTiyPq3dojqt6apehx0CMjYl7J++eBLQquc6XR1tbGaV88m5tuvJz+/frx68t+x2OPPdHqsKwFvnruD5jywEMsXLiYvQ49hi8c9ymO/9QnOP2b3+PqG25lw/WHc8F3vtHqMHu1FP9kV5F9mpL+B9gcmET27z8S+HtEnFLpWndxWFden3tPq0OwBA1cd7MeP7Dqk+84rOqcc/nT1zTlAVmFtqAj4mRJhwG757vGRcQ1RdZpZlaPZo7OqFYzpnpPB5ZExO2SVpc0OCI85cnMkrIswQRd6DhoSZ8HrgL+N981Ari2yDrNzOqR4jjooieqnATsAiwGiIhZZEPvzMyS0qiZhJI2kXSXpJmSHpV0Wr0xFd3F8WZEvNUx4ULSANK8WWpmfVwDB0wsA06PiOmSBgPTJP0xIh6rtaCiW9B/knQWMEjSR4ArgesLrtPMrGaNWiwpIuZFxPT89RJgJln3bs2KTtBnAPOBh4ETgJuAswuu08ysZm1E1ZuksZKmlmxjuypT0kjgA8Bf6omp6GF27cAv8s3MLFm1LCNauixFdyStCfwe+GJELK4npqIWS3qYMn3NEfH+Iuo1M6tXIyftSRpIlpwndrc4XDWKakEfmH/teATI+Pzr0cBrBdVpZla3Ri2WpGxUxKXAzIi4oCdlFZKgI+JpAEm7RMQuJYfOkHQfcF4R9ZqZ1auB45t3AT4FPCxpRr7vrIi4qdaCih5mt4akXSPiXgBJOwN9e5FnM0tSox5llee7hqzVUXSCPg74paSOhWoXAp8ruE4zs5q1RXorQhc9imMasI2kIWQr5/mZPGaWpD63WJKkVYHDgZHAgI4ZhRHhPmgzS0ozF+KvVtFdHNcBi4BpwJsF12VmVrf00nPxCXrjiNi34DrMzHqsUTcJG6noqd7/J+l9BddhZtZjjVqLo5GKbkHvCnxW0myyLg4B4ZmEZpaaPjeKA9iv4PLNzBqiz43iKJlRuB6wWpF1mZn1RJEP0K5X0Y+8OljSLGA28CfgKeDmIus0M6tHin3QRd8kPB/YEXgiIkYBewH3FVynmVnNIqLqrVmKTtBLI2IB0E9Sv4i4CxhdcJ1mZjVro73qrVmKvkm4MF+0+m5goqQXyJ7XZWaWlBRnEhbdgj4EeB34EnAL8A/goILrNDOrWdTwX7MUPYrj1ZK3lxVZl5lZT6TYgi7qkVdL6Hpqe8dElSFF1GtmVq8+Mw46IgYXUa6ZWVH6TAvazKy36YtTvc3MeoU+08VhZtbbhFvQZmZpSnE9aCdoMzPSXCzJCdrMDLegzcyS1dbuPmgzsyR5FIeZWaLcB21mlij3QZuZJcotaDOzRPkmoZlZotzFYWaWKHdxmJklysuNmpklyuOgzcwS5Ra0mVmi2hNcbrTop3qbmfUKEVH1VomkfSX9TdLfJZ1Rb0xuQZuZ0bhRHJL6AxcDHwHmAFMk/SEiHqu1LLegzcyAqGGrYAfg7xHxZES8BfwWOKSemJJtQS976zm1OoZUSBobEeNaHYelxZ+Lxqol50gaC4wt2TWu5GcxAni25Ngc4EP1xOQWdO8wtvIp1gf5c9EiETEuIrYr2Up/UXaV6OvqP3GCNjNrrDnAJiXvNwbm1lOQE7SZWWNNATaXNErSKsCRwB/qKSjZPmhbgfsZrSv+XCQoIpZJOhm4FegP/DIiHq2nLKW4QIiZmbmLw8wsWU7QZmaJcoLuAUnfkvSV/PV5kvbu4pwxkm5oUH1nlTn2lKR1G1TPK40ox+rTqO+/pJGSHmlEWdYaTtANEhHnRMTtBVfTbYI2s5WPE3SNJH0jXwTldmDLkv2/lvTx/PW+kh6XdC/wsW7K+aykqyXdImmWpP8oOXaUpIclPSLph/m+HwCDJM2QNLFCjNdKmibp0XzGU8f+VyR9V9KDkv4saf18/yhJ90uaIun8Hnx7rIEkrSnpDknT88/DIfn+kZJmSvpF/jO+TdKg/NgH85/v/cBJLf0HWI85QddA0gfJxjR+gCzxbt/FOasBvwAOAnYDNihT5GjgCOB9wBGSNpG0EfBDYM/8+PaSDo2IM4DXI2J0RBxdIdTPRcQHge2AUyWtk+9fA/hzRGwD3A18Pt9/EfCziNge+GeFsq153gAOi4htgT2AH0vqmKW2OXBxRGwFLAQOz/f/Cjg1InZqdrDWeE7QtdkNuCYiXouIxXQ9+PzdwOyImBXZGMYJZcq7IyIWRcQbwGPAO8iS/uSImB8Ry4CJwO41xnmqpAeBP5PNaNo83/8W0NEfPg0Ymb/eBZiUvx5fY11WHAHfk/QQcDvZGg/r58dmR8SM/PU0YKSkocBaEfGnfL9/lr2cJ6rUrpqB49UOLn+z5HUb2c+jR4tESRoD7A3sFBGvSZoMrJYfXhrLB7531NfBA+LTczQwHPhgRCyV9BTLf5adPzuDyD47/jmuRNyCrs3dwGGSBkkaTNaN0dnjwChJ78zfH1VjHX8BPixp3Xxd2aOAjhbRUkkDK1w/FHg5T87vBnasos77yLpuIEsKloahwAt5ct6D7C+sbkXEQmCRpF3zXf5Z9nJO0DWIiOnA74AZwO+Be7o45w2yVcZuzG8SPl1jHfOAM4G7gAeB6RFxXX54HPBQhZuEtwAD8j+Lzyfr5qjkNOAkSVPIkoKlYSKwnaSpZMn28SquORa4OL9J+HqRwVnxPNXbzCxRbkGbmSXKCdrMLFFO0GZmiXKCNjNLlBO0mVminKDtX0hqy9f8eETSlZJW70FZpWuUXCLpvWXOHSNp5zrq6HIlv2pW+Kt15bjSFQzNiuYEbV3pWPNja7Lp4SeWHswn0NQsIo6PiMfKnDIGqDlBm62snKCtknuAd+Wt27skXQ48LKm/pP/MV8B7SNIJAMr8j6THJN0IrNdRkKTJkrbLX++br9L2YL5i20iyXwRfylvvu0kaLun3eR1TJO2SX7tOvoLbA5L+lyqmx3e3wl9+7Md5LHdIGp7ve6eylQanSbonn5XZucxT83/nQ5J+W+f316xbXovDuiVpALAf2exEgB2ArSNidp7kFkXE9pJWBe6TdBvZSn9bkq3Qtz7ZIlC/7FTucLIV/3bPyxoWES9J+jnwSkT8KD/vcuC/IuJeSZuSPYTzPcC5wL0RcZ6kA8hmblbyubyOQcAUSb+PiAVkK/xNj4jTJZ2Tl30y2azNEyNilqQPAT8lW2Gw1BnAqIh4U9Ja1XxPzWrhBG1dGSRpRv76HuBSsq6Hv0bE7Hz/R4H3d/Qvk00R35xs5b1JEdEGzJV0Zxfl7wjc3VFWRLzUTRx7A+9dvsImQ/I1UHYnX2c7Im6U9HIV/6ZTJR2Wv+5Y4W8B0E42fR+ylQevlrRm/u+9sqTuVbso8yFgoqRrgWuriMGsJk7Q1pXXI2J06Y48Ub1augs4JSJu7XTe/lReUa3aVdf6ka3Kt8KaEnksVa9RUGGFv84ir3dh5+9BFw4g+2VxMPBNSVvlS8SaNYT7oK1etwL/3rG6nqQtJK1BtuLfkXkf9YZkC813dj/Zin2j8muH5fuXAINLzruNrLuB/LzR+cu7yVdqk7QfsHaFWMut8NcP6Pgr4JNkXSeLgdmS/i2vQ5K2KS1QUj9gk4i4C/gasBawZoU4zGriFrTV6xKyBf+nK2vSzgcOBa4h66t9GHiC5Uulvi0i5ud92Ffnie4F4CPA9cBVyh7tdApwKtnKbA+RfVbvJruR+G1gkqTpefnPVIj1FuDEvJy/seIKf68CW0maBiwie8INZL8AfibpbGAg8Fuy1QU79AcmKFskX2R95QsrxGFWE69mZ2aWKHdxmJklygnazCxRTtBmZolygjYzS5QTtJlZopygzcwS5QRtZpao/wd4SYFjPI4GKAAAAABJRU5ErkJggg==\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "yhat = svm_cv.predict(X_test)\n",
    "plot_confusion_matrix(Y_test,yhat)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  10\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Create a k nearest neighbors object then  create a  <code>GridSearchCV</code> object  <code>knn_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [],
   "source": [
    "parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],\n",
    "              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],\n",
    "              'p': [1,2]}\n",
    "\n",
    "KNN = KNeighborsClassifier()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {
    "collapsed": true,
    "jupyter": {
     "outputs_hidden": true
    },
    "tags": []
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
    }
   ],
   "source": [
    "knn_cv = GridSearchCV(KNN, parameters, scoring='accuracy', cv=10)\n",
    "knn_cv = knn_cv.fit(X_train, Y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "tuned hpyerparameters :(best parameters)  {'algorithm': 'auto', 'n_neighbors': 4, 'p': 1}\n",
      "accuracy : 0.875\n"
     ]
    }
   ],
   "source": [
    "print(\"tuned hpyerparameters :(best parameters) \",knn_cv.best_params_)\n",
    "print(\"accuracy :\",knn_cv.best_score_)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  11\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Calculate the accuracy of tree_cv on the test data using the method <code>score</code>:\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/home/jupyterlab/conda/envs/python/lib/python3.7/site-packages/sklearn/neighbors/base.py:442: DeprecationWarning: distutils Version classes are deprecated. Use packaging.version instead.\n",
      "  old_joblib = LooseVersion(joblib_version) < LooseVersion('0.12')\n",
      "/home/jupyterlab/conda/envs/python/lib/python3.7/site-packages/sklearn/neighbors/base.py:442: DeprecationWarning: distutils Version classes are deprecated. Use packaging.version instead.\n",
      "  old_joblib = LooseVersion(joblib_version) < LooseVersion('0.12')\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "0.7777777777777778"
      ]
     },
     "execution_count": 33,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "knn_accuracy = knn_cv.score(X_test, Y_test)\n",
    "knn_accuracy"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We can plot the confusion matrix\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/home/jupyterlab/conda/envs/python/lib/python3.7/site-packages/sklearn/neighbors/base.py:442: DeprecationWarning: distutils Version classes are deprecated. Use packaging.version instead.\n",
      "  old_joblib = LooseVersion(joblib_version) < LooseVersion('0.12')\n",
      "/home/jupyterlab/conda/envs/python/lib/python3.7/site-packages/sklearn/neighbors/base.py:442: DeprecationWarning: distutils Version classes are deprecated. Use packaging.version instead.\n",
      "  old_joblib = LooseVersion(joblib_version) < LooseVersion('0.12')\n"
     ]
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "yhat = knn_cv.predict(X_test)\n",
    "plot_confusion_matrix(Y_test,yhat)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## TASK  12\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Find the method performs best:\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Best Algorithm is Tree with a score of 0.9166666666666666\n",
      "Best Params is Tree: {'criterion': 'gini', 'max_depth': 4, 'max_features': 'auto', 'min_samples_leaf': 1, 'min_samples_split': 5, 'splitter': 'best'}\n"
     ]
    }
   ],
   "source": [
    "algorithms = {'KNN':knn_cv.best_score_,'Tree':tree_cv.best_score_,'LogisticRegression':logreg_cv.best_score_}\n",
    "bestalgorithm = max(algorithms, key=algorithms.get)\n",
    "print('Best Algorithm is',bestalgorithm,'with a score of',algorithms[bestalgorithm])\n",
    "if bestalgorithm == 'Tree':\n",
    "    print('Best Params is Tree:',tree_cv.best_params_)\n",
    "if bestalgorithm == 'KNN':\n",
    "    print('Best Params is KNN:',knn_cv.best_params_)\n",
    "if bestalgorithm == 'LogisticRegression':\n",
    "    print('Best Params is LogReg:',logreg_cv.best_params_)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Authors\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<a href=\"https://www.linkedin.com/in/joseph-s-50398b136/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork26802033-2022-01-01\">Joseph Santarcangelo</a> has a PhD in Electrical Engineering, his research focused on using machine learning, signal processing, and computer vision to determine how videos impact human cognition. Joseph has been working for IBM since he completed his PhD.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Change Log\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "| Date (YYYY-MM-DD) | Version | Changed By    | Change Description      |\n",
    "| ----------------- | ------- | ------------- | ----------------------- |\n",
    "| 2021-08-31        | 1.1     | Lakshmi Holla | Modified markdown       |\n",
    "| 2020-09-20        | 1.0     | Joseph        | Modified Multiple Areas |\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Copyright © 2020 IBM Corporation. All rights reserved.\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python",
   "language": "python",
   "name": "conda-env-python-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
