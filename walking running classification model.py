{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# PROJECT CODE: PRCP-1013-WalkRunClass\n",
    "# PROJECT NAME: Walking Running Classification\n",
    "## PROJECT TEAM ID: PTID-CDS-JUL21-1172\n",
    "#### Problem definition:\n",
    "To build an Long Short memory network to detect whether the person is running or walking based on sensor data collected from accelrometer and gyroscope."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# INTRODUCTION\n",
    "The given dataset contains a single file which represents 88588 sensor data samples collected from accelerometer and gyroscope at different points in time.This data is represented by following columns (each column contains sensor data for one of the sensor's axes):\n",
    "\n",
    "acceleration_x\n",
    "acceleration_y\n",
    "acceleration_z\n",
    "gyro_x\n",
    "gyro_y\n",
    "gyro_z\n",
    "There is an activity type represented by \"activity\" column which acts as label and reflects following activities:\n",
    "\n",
    "\"0\": walking\n",
    "\n",
    "\"1\": running\n",
    "\n",
    "Apart of that, the dataset contains \"wrist\" column which represents the wrist where the device was placed to collect a sample on:\n",
    "\n",
    "\"0\": left wrist\n",
    "\n",
    "\"1\": right wrist"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# STEP 1: IMPORT NECESSARY LIBRARIES AND PACKAGES"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import tensorflow as tf\n",
    "from tensorflow import keras\n",
    "import seaborn as sns\n",
    "import warnings\n",
    "from xgboost import XGBClassifier\n",
    "from tensorflow.keras.models import Sequential\n",
    "from tensorflow.keras.layers import Dense,Dropout,LSTM\n",
    "from sklearn.metrics import accuracy_score\n",
    "from tensorflow.keras.models import load_model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "warnings.filterwarnings('ignore')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## STEP 2: LOAD THE DATASET"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "C:\\Users\\arshad\\Downloads\\PRCP-1013-WalkRunClass\\Data\n"
     ]
    }
   ],
   "source": [
    "cd \"C:\\Users\\arshad\\Downloads\\PRCP-1013-WalkRunClass\\Data\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "data=pd.read_csv('walkrun.csv')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "##  STEP 3: EXPLORATORY DATA ANALYSIS"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
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
       "      <th>date</th>\n",
       "      <th>time</th>\n",
       "      <th>username</th>\n",
       "      <th>wrist</th>\n",
       "      <th>activity</th>\n",
       "      <th>acceleration_x</th>\n",
       "      <th>acceleration_y</th>\n",
       "      <th>acceleration_z</th>\n",
       "      <th>gyro_x</th>\n",
       "      <th>gyro_y</th>\n",
       "      <th>gyro_z</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>2017-6-30</td>\n",
       "      <td>13:51:15:847724020</td>\n",
       "      <td>viktor</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0.2650</td>\n",
       "      <td>-0.7814</td>\n",
       "      <td>-0.0076</td>\n",
       "      <td>-0.0590</td>\n",
       "      <td>0.0325</td>\n",
       "      <td>-2.9296</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2017-6-30</td>\n",
       "      <td>13:51:16:246945023</td>\n",
       "      <td>viktor</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0.6722</td>\n",
       "      <td>-1.1233</td>\n",
       "      <td>-0.2344</td>\n",
       "      <td>-0.1757</td>\n",
       "      <td>0.0208</td>\n",
       "      <td>0.1269</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>2017-6-30</td>\n",
       "      <td>13:51:16:446233987</td>\n",
       "      <td>viktor</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0.4399</td>\n",
       "      <td>-1.4817</td>\n",
       "      <td>0.0722</td>\n",
       "      <td>-0.9105</td>\n",
       "      <td>0.1063</td>\n",
       "      <td>-2.4367</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>2017-6-30</td>\n",
       "      <td>13:51:16:646117985</td>\n",
       "      <td>viktor</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0.3031</td>\n",
       "      <td>-0.8125</td>\n",
       "      <td>0.0888</td>\n",
       "      <td>0.1199</td>\n",
       "      <td>-0.4099</td>\n",
       "      <td>-2.9336</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>2017-6-30</td>\n",
       "      <td>13:51:16:846738994</td>\n",
       "      <td>viktor</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0.4814</td>\n",
       "      <td>-0.9312</td>\n",
       "      <td>0.0359</td>\n",
       "      <td>0.0527</td>\n",
       "      <td>0.4379</td>\n",
       "      <td>2.4922</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "        date                time username  wrist  activity  acceleration_x  \\\n",
       "0  2017-6-30  13:51:15:847724020   viktor      0         0          0.2650   \n",
       "1  2017-6-30  13:51:16:246945023   viktor      0         0          0.6722   \n",
       "2  2017-6-30  13:51:16:446233987   viktor      0         0          0.4399   \n",
       "3  2017-6-30  13:51:16:646117985   viktor      0         0          0.3031   \n",
       "4  2017-6-30  13:51:16:846738994   viktor      0         0          0.4814   \n",
       "\n",
       "   acceleration_y  acceleration_z  gyro_x  gyro_y  gyro_z  \n",
       "0         -0.7814         -0.0076 -0.0590  0.0325 -2.9296  \n",
       "1         -1.1233         -0.2344 -0.1757  0.0208  0.1269  \n",
       "2         -1.4817          0.0722 -0.9105  0.1063 -2.4367  \n",
       "3         -0.8125          0.0888  0.1199 -0.4099 -2.9336  \n",
       "4         -0.9312          0.0359  0.0527  0.4379  2.4922  "
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "date              0\n",
       "time              0\n",
       "username          0\n",
       "wrist             0\n",
       "activity          0\n",
       "acceleration_x    0\n",
       "acceleration_y    0\n",
       "acceleration_z    0\n",
       "gyro_x            0\n",
       "gyro_y            0\n",
       "gyro_z            0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# checking null values\n",
    "data.isnull().sum()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "'Date','Time','Username', and 'wrist' can be removed as it is obvious 'that they don't affect the target variable('Activity')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "data=data.iloc[:,4:]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
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
       "      <th>activity</th>\n",
       "      <th>acceleration_x</th>\n",
       "      <th>acceleration_y</th>\n",
       "      <th>acceleration_z</th>\n",
       "      <th>gyro_x</th>\n",
       "      <th>gyro_y</th>\n",
       "      <th>gyro_z</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>0.2650</td>\n",
       "      <td>-0.7814</td>\n",
       "      <td>-0.0076</td>\n",
       "      <td>-0.0590</td>\n",
       "      <td>0.0325</td>\n",
       "      <td>-2.9296</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>0</td>\n",
       "      <td>0.6722</td>\n",
       "      <td>-1.1233</td>\n",
       "      <td>-0.2344</td>\n",
       "      <td>-0.1757</td>\n",
       "      <td>0.0208</td>\n",
       "      <td>0.1269</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>0</td>\n",
       "      <td>0.4399</td>\n",
       "      <td>-1.4817</td>\n",
       "      <td>0.0722</td>\n",
       "      <td>-0.9105</td>\n",
       "      <td>0.1063</td>\n",
       "      <td>-2.4367</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>0</td>\n",
       "      <td>0.3031</td>\n",
       "      <td>-0.8125</td>\n",
       "      <td>0.0888</td>\n",
       "      <td>0.1199</td>\n",
       "      <td>-0.4099</td>\n",
       "      <td>-2.9336</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>0</td>\n",
       "      <td>0.4814</td>\n",
       "      <td>-0.9312</td>\n",
       "      <td>0.0359</td>\n",
       "      <td>0.0527</td>\n",
       "      <td>0.4379</td>\n",
       "      <td>2.4922</td>\n",
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
       "    </tr>\n",
       "    <tr>\n",
       "      <th>88583</th>\n",
       "      <td>0</td>\n",
       "      <td>0.3084</td>\n",
       "      <td>-0.8376</td>\n",
       "      <td>-0.1327</td>\n",
       "      <td>0.4823</td>\n",
       "      <td>2.0124</td>\n",
       "      <td>0.6048</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>88584</th>\n",
       "      <td>0</td>\n",
       "      <td>0.4977</td>\n",
       "      <td>-1.0027</td>\n",
       "      <td>-0.4397</td>\n",
       "      <td>0.1022</td>\n",
       "      <td>-1.2565</td>\n",
       "      <td>-0.0761</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>88585</th>\n",
       "      <td>0</td>\n",
       "      <td>0.4587</td>\n",
       "      <td>-1.1780</td>\n",
       "      <td>-0.2827</td>\n",
       "      <td>-1.4500</td>\n",
       "      <td>-0.2792</td>\n",
       "      <td>-1.2616</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>88586</th>\n",
       "      <td>0</td>\n",
       "      <td>0.2590</td>\n",
       "      <td>-0.8582</td>\n",
       "      <td>-0.0759</td>\n",
       "      <td>-1.5165</td>\n",
       "      <td>0.4560</td>\n",
       "      <td>-1.7755</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>88587</th>\n",
       "      <td>0</td>\n",
       "      <td>0.3140</td>\n",
       "      <td>-0.8008</td>\n",
       "      <td>-0.0911</td>\n",
       "      <td>0.1183</td>\n",
       "      <td>1.0850</td>\n",
       "      <td>1.2814</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>88588 rows × 7 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "       activity  acceleration_x  acceleration_y  acceleration_z  gyro_x  \\\n",
       "0             0          0.2650         -0.7814         -0.0076 -0.0590   \n",
       "1             0          0.6722         -1.1233         -0.2344 -0.1757   \n",
       "2             0          0.4399         -1.4817          0.0722 -0.9105   \n",
       "3             0          0.3031         -0.8125          0.0888  0.1199   \n",
       "4             0          0.4814         -0.9312          0.0359  0.0527   \n",
       "...         ...             ...             ...             ...     ...   \n",
       "88583         0          0.3084         -0.8376         -0.1327  0.4823   \n",
       "88584         0          0.4977         -1.0027         -0.4397  0.1022   \n",
       "88585         0          0.4587         -1.1780         -0.2827 -1.4500   \n",
       "88586         0          0.2590         -0.8582         -0.0759 -1.5165   \n",
       "88587         0          0.3140         -0.8008         -0.0911  0.1183   \n",
       "\n",
       "       gyro_y  gyro_z  \n",
       "0      0.0325 -2.9296  \n",
       "1      0.0208  0.1269  \n",
       "2      0.1063 -2.4367  \n",
       "3     -0.4099 -2.9336  \n",
       "4      0.4379  2.4922  \n",
       "...       ...     ...  \n",
       "88583  2.0124  0.6048  \n",
       "88584 -1.2565 -0.0761  \n",
       "88585 -0.2792 -1.2616  \n",
       "88586  0.4560 -1.7755  \n",
       "88587  1.0850  1.2814  \n",
       "\n",
       "[88588 rows x 7 columns]"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data"
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
       "<seaborn.axisgrid.PairGrid at 0x24357d98bb0>"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
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\n",
      "text/plain": [
       "<Figure size 1124.88x1080 with 42 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "sns.pairplot(data,hue='activity')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "None of the independent variables seem to be correlated to each other"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[11:05:38] WARNING: C:/Users/Administrator/workspace/xgboost-win64_release_1.4.0/src/learner.cc:1095: Starting in XGBoost 1.3.0, the default evaluation metric used with the objective 'binary:logistic' was changed from 'error' to 'logloss'. Explicitly set eval_metric if you'd like to restore the old behavior.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,\n",
       "              colsample_bynode=1, colsample_bytree=1, gamma=0, gpu_id=-1,\n",
       "              importance_type='gain', interaction_constraints='',\n",
       "              learning_rate=0.300000012, max_delta_step=0, max_depth=6,\n",
       "              min_child_weight=1, missing=nan, monotone_constraints='()',\n",
       "              n_estimators=100, n_jobs=4, num_parallel_tree=1, random_state=0,\n",
       "              reg_alpha=0, reg_lambda=1, scale_pos_weight=1, subsample=1,\n",
       "              tree_method='exact', validate_parameters=1, verbosity=None)"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# checking feature importances using xgboost\n",
    "x=data.iloc[:,1:]\n",
    "y=data['activity']\n",
    "XGB=XGBClassifier()\n",
    "XGB.fit(x,y)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([0.05115017, 0.5802132 , 0.2824638 , 0.02609092, 0.01136927,\n",
       "       0.04871267], dtype=float32)"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "XGB.feature_importances_"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x360 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(6,5))\n",
    "plt.bar(range(len(XGB.feature_importances_)),XGB.feature_importances_)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "'acceleration_y' and 'gyro_y' appears to be the most and least important features respectively.Since all the features affects the target variable, though by different extents, and they do not possess any visible correlation between each other, there is no need for any feature elimination."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<AxesSubplot:xlabel='gyro_z'>"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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UZeBwLZs2SIp+fyWOzOTu3ebNmbMGHV2dioWi2Ven01NTbr11lv12muv6ZprrpGZae3atXrLW96iRYsW6aWXXtLSpUv1wAMP6LLLLtOqVas0fPhw3XTTTfq7v/s77dy5U5J022236dRTT82MD3/xF3+Rd3zatGmTvvSlL2ny5Mm69dZbNWbMmMzYcuaZZ6qhoUGLFi3S7bffLnfXokWLtGbNmoLGvFAGMs6ivJT7c5ervvS0BQsWZI711157TQsXLtTq1avV3NysRCKha665JvO6bmxsVFdXl3bv3q1x48bplVde6fWar6ur04kTJzRlypSS7ydQTPv379fevXtz9uNc/a++vl5jxozRyy+/rOXLl+vkk0/Wl770Jbm7li1bph/84AdasGCBbrvtNh05ckQdHR0aNmyYVq1apbvuuktdXV1yd9XX12vVqlWSVNA4U+7j0WCVYr+s55NYiJkzZ/qmTZsGvdHbb79dDz/8sObNm6drr712UPNeeeWVam9vlyTFYjF1dXVl7ovH45n70rfvvvvuXsvlOohzLZ9Lz21Wo0oJWQsXLtTmna/o0DlzB7zsyB3rJWnQy76raZxWr1494GWjUgnhajAuvfRSbdmyJfO6jcfjOvfcc/XQQw9JUiaU1dXVZV63o0eP1htvvJFZx+jRozV27NjMOi699NK849PFF1+cWTY9X/bYkq4hu55du3YVNOaFMpBxtj9mttndZwYqreqVskdGIVd96WmTJk3KHOvp12S6B/d8jQxEQ0ODHn300YB7UbmG0vP6MpR+WMi6K61fFttQ+nEsFtOIESMyfSjd4yZNmtTrNdaz10nJvuXuBY0z5T4eDVao/eqrP5b8csHOzk5t2LBB7q4NGzaos7NzwPMmEoluB1HPsNPzAGtvb1cikei1XL6AWUgTqPaAJVXvG/JaVc3P58MPP9ztddve3q6HH344czv9CV7267Zn03njjTe6rWP9+vU5x6dNmzZ1W3b9+vXatGlTznEn++9CxrxQBjLOoryU+3OXq77saeljff369ZnXQHt7u3784x8POmBJ0pEjR5RIJMLsBBCxBx98cEjLd3V1detD6R6X6zXWs9dJyb5VyDhT7uPRYJVqv0p+ueC6det04sQJSdLx48d1zz335E2Q+eZta2sb8HYHswySn5iVu0QioWFHB35GdqiGHf4vJRK/qYjH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\n",
      "text/plain": [
       "<Figure size 1080x720 with 6 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(15,10))\n",
    "plt.subplot(3,2,1)\n",
    "sns.boxplot(data['acceleration_x'])\n",
    "plt.subplot(3,2,2)\n",
    "sns.boxplot(data['acceleration_y'])\n",
    "plt.subplot(3,2,3)\n",
    "sns.boxplot(data['acceleration_z'])\n",
    "plt.subplot(3,2,4)\n",
    "sns.boxplot(data['gyro_x'])\n",
    "plt.subplot(3,2,5)\n",
    "sns.boxplot(data['gyro_y'])\n",
    "plt.subplot(3,2,6)\n",
    "sns.boxplot(data['gyro_z'])\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "As most of the datapoints of all the features are more or less clustered, we can conclude that there are only few outliers, which can be seen as isolated points in the boxplots."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "# removing the outliers\n",
    "data['acceleration_x'][data['acceleration_x']>4.5]= data['acceleration_x'].mean()\n",
    "data['acceleration_y'][data['acceleration_y']<-3]= data['acceleration_y'].mean()\n",
    "data['acceleration_z'][data['acceleration_z']<-3.5]= data['acceleration_z'].mean()\n",
    "data['gyro_y'].loc[(data['gyro_y']<-7)|(data['gyro_y']>8)]= data['gyro_y'].mean()\n",
    "data['gyro_z'].loc[(data['gyro_z']<-9)|(data['gyro_z']>8)]= data['gyro_z'].mean()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<AxesSubplot:xlabel='gyro_z'>"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAA1YAAAJNCAYAAAAyOuSHAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjMuMiwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8vihELAAAACXBIWXMAAAsTAAALEwEAmpwYAABC6klEQVR4nO3df5iddX0n/PcnTJIB0x9QQCAhIZNH0qU/tF36a/tjsQaWWmW7dX2a7trVthe6qK2riYaIuvvUVQGDLV7SbsFau9Y1W1ttq22VYLVun6f1KVgpVIuPDiUEUNHYbgEDhHyfP+aHM5OZyUzumTlnJq/XdXFlzne+574/5+bM9zPvc9/nTLXWAgAAwPFb1esCAAAAljvBCgAAoCPBCgAAoCPBCgAAoCPBCgAAoCPBCgAAoKOB+Uw+/fTT23nnnbdIpQDQL2677bYvt9bO6HUdy4X+CHDimKlHzitYnXfeebn11lsXrioA+lJV3dPrGpYT/RHgxDFTj3QpIAAAQEeCFQAAQEeCFQAAQEeCFQAAQEeCFQAAQEeCFQAAQEeCFQAAQEeCFQAAQEeCFQAAQEeCFQAAQEeCFQAAQEeCFQAAQEeCFQAAQEcDvS4Aloubbropw8PDc5r7wAMPJEnOPvvs49rX0NBQLr/88uO6LwCLYz59YDZde8RC0WtgYQlWMEfDw8P5/O23Z/2hQ8ec+/DgYJLk0P79897PfaP3BaC/zKcPzKZLj1goeg0sPMEK5mH9oUN52d13H3Pe9Zs3J8mc5s50XwD6z1z7wGy69IiFotfAwvMeKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EKwAAgI4EK/rKTTfdlJtuuqnXZTAD/39gZfEzDfPjZ4bZDPS6AJhoeHi41yUwC/9/YGXxMw3z42eG2ThjBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0JFgBQAA0NHAUu7s4MGDufbaa7Nr166ceuqp04631o6ac/DgwbzhDW9IVeWqq64an/OiF70ov/Irv5L7778/3/zN35wvfvGLef3rX58jR47kv/yX/5LnPOc5ee973/v1BzswkMOHD49/fdJJJ+Ubv/Eb8+CDDy7lYWAO3vzmN+eVr3xlr8tgijvvvDNJ8uxnP7vHlawsq1atyurVq3PWWWfl8OHDuf/++/PkJz85X/nKV/L4448nSZ7//Ofnv//3/541a9bkZS97Wa6//vo8+uijWb9+fdatW5fLLrss1113XXbu3Jk/+qM/Omqdpf9N7ZEHDx7MG9/4xrTW8tKXvjS//uu/Pmv/HBsfHh7Orl27kiSvec1r8p73vGe8v/7SL/1S7r333jz++OPZuHFjBgcHs3r16p48XliOVmofPPXUU/PVr341SXLSSSfliSeeGP/eqlWrcuTIkTzrWc/KBz/4waxZsyavfe1r8853vjP33XdfzjrrrPE+9rznPS9vetObsnv37rzrXe9KVeUlL3lJ3va2t+WJJ57Io48+mgMHDmTNmjU588wz8+UvfzlnnnlmTj755Fx11VUz9q2pWWC2dXDs9gtf+MLceOONR40vZn9c0jNWe/fuzac//ens3bt3xvHp5uzduzef/exnc9ddd02as2fPngwPD+fQoUP5whe+kNZarr766lxzzTU5cuTIpFCVZDxUjX396KOPClV96uMf/3ivS4Alc+TIkTz66KO55557ct9996W1li984QvjoSpJfuu3fiuttTz66KN5y1vekkcffTRJct999+Wuu+7KL//yL+fIkSN5y1veMu06S/+b2v/27t2bu+66K5/97GezZ8+eY/bPMXv27MmhQ4dy6NChXH311ZP66+c///k89thjaa3lnnvu0QOBJBkPVUkmhapkpEclyQc/+MEkyWOPPZZrrrkmn//853Po0KH8/d//fYaHh3PXXXfl6quvziOPPJJrrrlm/Hf3PXv25LOf/Ww+//nP58CBA+PbOHDgQA4dOpT9+/eP/44/k6lZYOr3pq6dn/70p3PddddNO76Y/XHJgtXBgwfzkY98JK213HLLLeP/AyeO79u3L7fccsukOQcPHswtt9wyvp2Jc/bv33/Ufh566KE8/PDDS/WwWERvfvObe10CE6y0V+eWs4kvEk0dO3z48FHrLP1vao8cHh6e1Pv2798/a/8cGx8eHs699947fr+HHnpovL/u27dv2v1ODPDAzPTBr3vooYemHR/7HXzi96f7fX06+/btm7ZvTZcFZloH77777vHbE9fNieOL2R+X7FLAvXv3jifeI0eOZO/evbniiismjU/8ZWFsTmtt0vjjjz+eqlqqsumhj3/84zl48GCvyxg3PDyc1WvWLPp+HlyzJo8PD2f37t2Lvi9WronrLP1vao+87rrrpg3QM/XPsfE77rhj2u2PBe7pfO5zn7PezNFS9YGloNfQbw4fPjxt39q7d+9RV53NtA7u2bNn/PaYqeOL2R+Pecaqql5YVbdW1a1dLhn42Mc+NukV1Y9+9KNHjbfWxhf+sTkf+9jHjmoGMzUHAEZMXGdZHAvVH5Oje+TYK61TzdQ/x8Ynnq2aaLa+OfWyH4BeaK1N27emZoGJ86ZbO6e+KDV1fDH74zHPWLXWbkxyY5JceOGFx51oLrroouzbty+HDx/OwMBAnv70px81PnYmqrU2Pqe1lg996EOTDmhVCVcniDe96U29LmHc7t27c+gTn1j0/Zzx2GMZHBrqq8eeuARiuZm4zrI4Fqo/Jkf3yHPOOSf33nvvUb1upv45Nn7HHXdMG65m65unnXZa3603/Wqp+sBS6Nde08/0wcVVVdP2rYsuumhSFpg4b7q18/77758UrqaOL2Z/XLL3WG3fvj2rVo3sbtWqVdm+fftR4wMDAxkYGJg0Z/v27eNjSbJ69epJt1m5fuRHfqTXJcCyNXGdpf9N7ZE7duyYttfN1D/Hxnfu3Dnt9if216nOOOOMhXgIAJ0MDAxM27emZoGJ86augzt37hy/PWbq+GL2xyULVqeddlqe8YxnpKqybdu28Y85nDh+8cUXZ9u2bZPmnHbaadm2bdv4dibO2bhx41H7WbduXZ70pCct1cNiEfm49f7ygQ98oNclMGq6X5DHxgYGBo5aZ+l/U3vk0NDQpN63cePGWfvn2PjQ0FDOPffc8futW7duvL9efPHF0+7Xx63D3OiDX7du3bppx8d+B5/4/el+X5/OxRdfPG3fmi4LzLQObt68efz2xHVz4vhi9scl/bj17du354ILLjgqJU4cn27O9u3bc/7552fr1q2T5uzcuTNDQ0MZHBzMWWedlarKlVdemV27dmXVqlV57nOfO2k/U9Pu2rVrvVLXp5yt4kSyatWqrF27Nps2bcr69etTVTnrrLMm/cL7/Oc/P1WVtWvX5hWveEXWrl2bJFm/fn22bt2al7/85Vm1alVe8YpXTLvO0v+m9r/t27dn69atOf/887Nz585j9s8xO3fuzODgYAYHB3PllVdO6q9btmzJmjVrUlXZtGmTHggkyaSgcdJJJ0363tiZnmc961lJkjVr1mTXrl3ZsmVLBgcHc95552VoaChbt27NlVdemVNOOSW7du0a/919586dOf/887Nly5Zs2LBhfBsbNmzI4OBgNm7cOP47/kymZoGp35u6dl5wwQXZsWPHtOOL2R9rPu9VuvDCC9utt966aMXA2KcT9eM132PX1r/s7ruPOff6zZuTZE5zp7vv4Pd9X98eg6Q///+wsKrqttbahb2uY7lYrv3Rz/T8zKcPzKZLj1go/dxr+pmfGZKZe+SSnrECAABYiQQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgQrAACAjgZ6XQBMNDQ01OsSmIX/P7Cy+JmG+fEzw2wEK/rK5Zdf3usSmIX/P7Cy+JmG+fEzw2xcCggAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANCRYAUAANDRQK8LgOXkvsHBXL958zHnHRgcTJI5zZ1uH1vmfS8AlsJc+8BsuvSIhaLXwMITrGCOhoaG5jz3SQ88kCQZPPvsee9nyzz3BcDSWKi1uUuPWCh6DSw8wQrm6PLLL+91CQD0kD4AzMZ7rAAAADoS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kWAFAADQ0cBS7uzgwYO59tpr88IXvjA33nhjdu3alVNPPXV8fNeuXWmtjc+54YYb8sQTT2RgYCBXXXVVTj311Enb2b59e970pjfl1a9+dd71rnfl8ccfT1XlkUceyQMPPDC+37PPPjurVq3K/fffnyuuuCLveMc78vjjj+eJJ55IklRVWmvj81evXp3HH398KQ8Ny8Szn/3sfOADH+h1GcvSnXfemWTkGC4Hq1atypEjR8b/neqMM87Igw8+mCTZsGFD1qxZk6997Wt54IEHsmHDhrzyla/MjTfemBe96EW54YYbxtecL3zhC2mtpapy1llnpbWWBx98MNdcc002b948bS0T18ip6+DEsdnG6X/Dw8PZvXt3rr766mzevDkHDx7MG97whjzxxBM56aST8tKXvjRve9vbxm+/5jWvSWstb3zjG3P48OE8/vjj+dKXvpRzzjknL3vZy/LWt741Bw4cSGstrbXxvnb22WfnlFNOyeHDh7N///601nL77bfnqU99ao+PANDvvvjFL+bBBx+cdy8/+eST87WvfW3G7w8MDOSkk07K6aefnq985Ss588wzs3r16jz66KM5cOBAzj333Jx88snj697EHHD11Vfnm77pm/LGN74xrbU873nPy9VXX53du3dn79690+aNxeqPSxqs9u7dm09/+tO57rrrcu+992bv3r254oorxsf37t2b1tr4nP3790+67xVXXDFpO9dcc00eeeSRXH311XnooYdm3O/EkPVrv/Zrk0JUkqNuC1XAWJiaLlQlGQ9VSXLgwIFJ3ztw4MD4Ordnz55Ja9lE99xzz/jXe/bsyQ033DDtvIlr5NR1cOLYbOP0vz179uSRRx4Zfy7s3bs3n/3sZyd9f2pfbK3lrrvumrSd4eHho3roRBN74pirr74673nPexbokQAr1cTeNx+zhaokOXz4cA4fPpz77rsvSY5av+69994kmZQVxnLAnj178m3f9m3ja+G1116bRx55JNdcc00efvjhafPGYvXHJbsU8ODBg/nIRz6S1tr4K2S33HJL7r777vHxffv25ZZbbhmfM9G+ffvy1a9+ddJ2xsLUbKFqqqkhCuZruZxx6Scn4jEbW+dm+uV2uvl33333UeMT17xbbrnlqHVwbGymuSwPw8PD47847N+/P7fffntuueWWSXOmPpduvvnmo+bMNPdYHnro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\n",
      "text/plain": [
       "<Figure size 1080x720 with 6 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(15,10))\n",
    "plt.subplot(3,2,1)\n",
    "sns.boxplot(data['acceleration_x'],color='r')\n",
    "plt.subplot(3,2,2)\n",
    "sns.boxplot(data['acceleration_y'],color='r')\n",
    "plt.subplot(3,2,3)\n",
    "sns.boxplot(data['acceleration_z'],color='r')\n",
    "plt.subplot(3,2,4)\n",
    "sns.boxplot(data['gyro_x'],color='r')\n",
    "plt.subplot(3,2,5)\n",
    "sns.boxplot(data['gyro_y'],color='r')\n",
    "plt.subplot(3,2,6)\n",
    "sns.boxplot(data['gyro_z'],color='r')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<AxesSubplot:xlabel='gyro_z', ylabel='Count'>"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1080x720 with 6 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "# checking skewness\n",
    "plt.figure(figsize=(15,10))\n",
    "plt.subplot(2,3,1)\n",
    "sns.histplot(data['acceleration_x'])\n",
    "plt.subplot(2,3,2)\n",
    "sns.histplot(data['acceleration_y'])\n",
    "plt.subplot(2,3,3)\n",
    "sns.histplot(data['acceleration_z'])\n",
    "plt.subplot(2,3,4)\n",
    "sns.histplot(data['gyro_x'])\n",
    "plt.subplot(2,3,5)\n",
    "sns.histplot(data['gyro_y'])\n",
    "plt.subplot(2,3,6)\n",
    "sns.histplot(data['gyro_z'])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "All features are almost normally distributed"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<AxesSubplot:xlabel='activity', ylabel='count'>"
      ]
     },
     "execution_count": 18,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAZIAAAEGCAYAAABPdROvAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjMuMiwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8vihELAAAACXBIWXMAAAsTAAALEwEAmpwYAAAQ2UlEQVR4nO3df6zddX3H8eeLFoFFYfwoyFpY2WjcgDkJHWOabcaa0f0SZkBrwuhmk24EnSabC5hsOk0X2dwYGGHpBCnMCB2iVBe2kCIziwgWRREYoRMHDYyWH0PYArPsvT/O5+rp5bYc+rnn3l7v85GcnO/3fb6fz/18ScMrn+/ne74nVYUkSXtrv9kegCRpbjNIJEldDBJJUheDRJLUxSCRJHVZONsDmGlHHHFELV26dLaHIUlzyp133vl4VS2a6rN5FyRLly5ly5Ytsz0MSZpTkvzH7j7z0pYkqYtBIknqYpBIkroYJJKkLgaJJKmLQSJJ6mKQSJK6GCSSpC4GiSSpy7z7Zvt0OOV9V8/2ELQPuvMvz53tIfDQh35mtoegfdCxf3r3WPt3RiJJ6mKQSJK6GCSSpC4GiSSpi0EiSepikEiSuhgkkqQuBokkqYtBIknqYpBIkroYJJKkLgaJJKmLQSJJ6mKQSJK6GCSSpC4GiSSpy9iDJMmCJF9P8oW2f1iSm5M80N4PHTr2wiRbk9yf5PSh+ilJ7m6fXZokrX5Akuta/fYkS8d9PpKkXc3EjOQ9wH1D+xcAm6tqGbC57ZPkBGAVcCKwErgsyYLW5nJgLbCsvVa2+hrgqao6HrgYuGi8pyJJmmysQZJkCfDrwCeGymcAG9r2BuDMofq1VfV8VT0IbAVOTXI0cHBV3VZVBVw9qc1EX9cDKyZmK5KkmTHuGcnfAH8M/N9Q7aiqehSgvR/Z6ouBh4eO29Zqi9v25PoubapqJ/A0cPjkQSRZm2RLki07duzoPCVJ0rCxBUmS3wC2V9WdozaZolZ7qO+pza6FqvVVtbyqli9atGjE4UiSRrFwjH2/AXhLkl8DDgQOTvL3wGNJjq6qR9tlq+3t+G3AMUPtlwCPtPqSKerDbbYlWQgcAjw5rhOSJL3Y2GYkVXVhVS2pqqUMFtFvqapzgE3A6nbYauDGtr0JWNXuxDqOwaL6He3y1zNJTmvrH+dOajPR11ntb7xoRiJJGp9xzkh25yPAxiRrgIeAswGq6p4kG4F7gZ3A+VX1QmtzHnAVcBBwU3sBXAFck2Qrg5nIqpk6CUnSwIwESVXdCtzatp8AVuzmuHXAuinqW4CTpqg/RwsiSdLs8JvtkqQuBokkqYtBIknqYpBIkroYJJKkLgaJJKmLQSJJ6mKQSJK6GCSSpC4GiSSpi0EiSepikEiSuhgkkqQuBokkqYtBIknqYpBIkroYJJKkLgaJJKmLQSJJ6mKQSJK6GCSSpC4GiSSpi0EiSepikEiSuhgkkqQuBokkqYtBIknqYpBIkroYJJKkLgaJJKmLQSJJ6mKQSJK6GCSSpC4GiSSpi0EiSepikEiSuhgkkqQuBokkqcvYgiTJgUnuSPKNJPck+bNWPyzJzUkeaO+HDrW5MMnWJPcnOX2ofkqSu9tnlyZJqx+Q5LpWvz3J0nGdjyRpauOckTwPvKmqfhZ4HbAyyWnABcDmqloGbG77JDkBWAWcCKwELkuyoPV1ObAWWNZeK1t9DfBUVR0PXAxcNMbzkSRNYWxBUgPPtt3926uAM4ANrb4BOLNtnwFcW1XPV9WDwFbg1CRHAwdX1W1VVcDVk9pM9HU9sGJitiJJmhljXSNJsiDJXcB24Oaquh04qqoeBWjvR7bDFwMPDzXf1mqL2/bk+i5tqmon8DRw+BTjWJtkS5ItO3bsmKazkyTBmIOkql6oqtcBSxjMLk7aw+FTzSRqD/U9tZk8jvVVtbyqli9atOglRi1Jejlm5K6tqvov4FYGaxuPtctVtPft7bBtwDFDzZYAj7T6kinqu7RJshA4BHhyHOcgSZraOO/aWpTkR9v2QcCbgX8DNgGr22GrgRvb9iZgVbsT6zgGi+p3tMtfzyQ5ra1/nDupzURfZwG3tHUUSdIMWTjGvo8GNrQ7r/YDNlbVF5LcBmxMsgZ4CDgboKruSbIRuBfYCZxfVS+0vs4DrgIOAm5qL4ArgGuSbGUwE1k1xvORJE1hbEFSVd8ETp6i/gSwYjdt1gHrpqhvAV60vlJVz9GCSJI0O/xmuySpi0EiSepikEiSuhgkkqQuBokkqYtBIknqYpBIkroYJJKkLgaJJKmLQSJJ6mKQSJK6GCSSpC4GiSSpi0EiSeoyUpAk2TxKTZI0/+zx90iSHAj8CHBEkkP5wW+kHwz82JjHJkmaA17qh61+D3gvg9C4kx8EyXeBj49vWJKkuWKPQVJVlwCXJHl3VX1shsYkSZpDRvqp3ar6WJLXA0uH21TV1WMalyRpjhgpSJJcA/wkcBfwQisXYJBI0jw3UpAAy4ETqqrGORhJ0twz6vdIvgW8epwDkSTNTaPOSI4A7k1yB/D8RLGq3jKWUUmS5oxRg+SD4xyEJGnuGvWurX8Z90AkSXPTqHdtPcPgLi2AVwD7A/9dVQePa2CSpLlh1BnJq4b3k5wJnDqOAUmS5pa9evpvVX0OeNP0DkWSNBeNemnrrUO7+zH4XonfKZEkjXzX1m8Obe8EvgOcMe2jkSTNOaOukfzuuAciSZqbRv1hqyVJPptke5LHknwmyZJxD06StO8bdbH9k8AmBr9Lshj4fKtJkua5UYNkUVV9sqp2ttdVwKIxjkuSNEeMGiSPJzknyYL2Ogd4YpwDkyTNDaMGyTuBtwH/CTwKnAW4AC9JGvn23w8Dq6vqKYAkhwEfZRAwkqR5bNQZyWsnQgSgqp4ETt5TgyTHJPlikvuS3JPkPa1+WJKbkzzQ3g8danNhkq1J7k9y+lD9lCR3t88uTZJWPyDJda1+e5KlL+PcJUnTYNQg2W/S//AP46VnMzuBP6yqnwZOA85PcgJwAbC5qpYBm9s+7bNVwInASuCyJAtaX5cDa4Fl7bWy1dcAT1XV8cDFwEUjno8kaZqMGiR/BXw5yYeTfAj4MvAXe2pQVY9W1dfa9jPAfQxuHT4D2NAO2wCc2bbPAK6tquer6kFgK3BqkqOBg6vqtvZTv1dPajPR1/XAionZiiRpZoz6zfark2xh8KDGAG+tqntH/SPtktPJwO3AUVX1aOv30SRHtsMWA18Zarat1b7XtifXJ9o83PrameRp4HDg8Ul/fy2DGQ3HHnvsqMOWJI1g1MV2WnCMHB4TkrwS+Azw3qr67h4mDFN9UHuo76nNroWq9cB6gOXLl/uwSUmaRnv1GPlRJdmfQYh8qqpuaOXH2uUq2vv2Vt8GHDPUfAnwSKsvmaK+S5skC4FDgCen/0wkSbsztiBpaxVXAPdV1V8PfbQJWN22VwM3DtVXtTuxjmOwqH5Huwz2TJLTWp/nTmoz0ddZwC1tHUWSNENGvrS1F94A/DZwd5K7Wu39wEeAjUnWAA8BZwNU1T1JNjK4fLYTOL+qXmjtzgOuAg4CbmovGATVNUm2MpiJrBrj+UiSpjC2IKmqf2XqNQyAFbtpsw5YN0V9C3DSFPXnaEEkSZodY10jkST98DNIJEldDBJJUheDRJLUxSCRJHUxSCRJXQwSSVIXg0SS1MUgkSR1MUgkSV0MEklSF4NEktTFIJEkdTFIJEldDBJJUheDRJLUxSCRJHUxSCRJXQwSSVIXg0SS1MUgkSR1MUgkSV0MEklSF4NEktTFIJEkdTFIJEldDBJJUheDRJLUxSCRJHUxSCRJXQwSSVIXg0SS1MUgkSR1MUgkSV0MEklSF4NEktTFIJEkdTFIJEldxhYkSa5Msj3Jt4ZqhyW5OckD7f3Qoc8uTLI1yf1JTh+qn5Lk7vbZpUnS6gckua7Vb0+ydFznIknavXHOSK4CVk6qXQBsrqplwOa2T5ITgFXAia3NZUkWtDaXA2uBZe010eca4KmqOh64GLhobGciSdqtsQVJVX0JeHJS+QxgQ9veAJw5VL+2qp6vqgeBrcCpSY4GDq6q26qqgKsntZno63pgxcRsRZI0c2Z6jeSoqnoUoL0f2eqLgYeHjtvWaovb9uT6Lm2qaifwNHD4VH80ydokW5Js2bFjxzSdiiQJ9p3F9qlmErWH+p7avLhYtb6qllfV8kWLFu3lECVJU5npIHmsXa6ivW9v9W3AMUPHLQEeafUlU9R3aZNkIXAIL76UJkkas5kOkk3A6ra9GrhxqL6q3Yl1HINF9Tva5a9nkpzW1j/OndRmoq+zgFvaOookaQYtHFfHST4NvBE4Isk24APAR4CNSdYADwFnA1TVPUk2AvcCO4Hzq+qF1tV5DO4AOwi4qb0ArgCuSbKVwUxk1bjORZK0e2MLkqp6x24+WrGb49cB66aobwFOmqL+HC2IJEmzZ19ZbJckzVEGiSSpi0EiSepikEiSuhgkkqQuBokkqYtBIknqYpBIkroYJJKkLgaJJKmLQSJJ6mKQSJK6GCSSpC4GiSSpi0EiSepikEiSuhgkkqQuBokkqYtBIknqYpBIkroYJJKkLgaJJKmLQSJJ6mKQSJK6GCSSpC4GiSSpi0EiSepikEiSuhgkkqQuBokkqYtBIknqYpBIkroYJJKkLgaJJKmLQSJJ6mKQSJK6GCSSpC4GiSSpy5wPkiQrk9yfZGuSC2Z7PJI038zpIEmyAPg48KvACcA7kpwwu6OSpPllTgcJcCqwtaq+XVX/C1wLnDHLY5KkeWXhbA+g02Lg4aH9bcDPTz4oyVpgbdt9Nsn9MzC2+eII4PHZHsS+IB9dPdtD0K78tznhA5mOXn58dx/M9SCZ6r9OvahQtR5YP/7hzD9JtlTV8tkehzSZ/zZnzly/tLUNOGZofwnwyCyNRZLmpbkeJF8FliU5LskrgFXAplkekyTNK3P60lZV7UzyLuCfgQXAlVV1zywPa77xkqH2Vf7bnCGpetGSgiRJI5vrl7YkSbPMIJEkdTFItFd8NI32VUmuTLI9ybdmeyzzhUGil81H02gfdxWwcrYHMZ8YJNobPppG+6yq+hLw5GyPYz4xSLQ3pno0zeJZGoukWWaQaG+M9GgaSfODQaK94aNpJH2fQaK94aNpJH2fQaKXrap2AhOPprkP2OijabSvSPJp4DbgNUm2JVkz22P6YecjUiRJXZyRSJK6GCSSpC4GiSSpi0EiSepikEiSuhgk0gxL8sYkrx/a//0k575Em09MPBgzyfvHPUbp5fD2X2mGJfkg8GxVfXQv2z9bVa+c3lFJe88gkaZJks8xeHTMgcAlVbU+yUrgz4EFwOPAGuArwAvADuDdwArgWeAfgQ1VdWrrbymwqapem+RW4I+As4D3AXcD9wDfBh6vqktam3XAY1V16QycsgTAwtkegPRD5J1V9WSSg4CvJrkR+Dvgl6rqwSSHtc//lqEZSZIVAFV1X5JXJPmJqvo28HZg4/AfqKoLkryrql7X2i4FbgAuSbIfg8fVnDozpysNuEYiTZ8/SPINBjOOY4C1wJeq6kGAqhrlNzI2Am9r228HrtvTwVX1HeCJJCcDvwJ8vaqe2LvhS3vHGYk0DZK8EXgz8AtV9T/tUtQ3gNe8zK6uA/4hyQ1AVdUDI7T5BPA7wKuBK1/m35O6OSORpschwFMtRH4KOA04APjlJMcBJDmsHfsM8KqpOqmqf2ewfvIn7H428r0k+w/tf5bBT8v+HIMHaUozyiCRpsc/AQuTfBP4MIPLWzsYXN66oV3ymgiGzwO/leSuJL84RV/XAecwaX1kyHrgm0k+BdB+7viLDJ7C/MJ0nZA0Ku/akua4tsj+NeDsES+FSdPKGYk0h7UvKW4FNhsimi3OSCRJXZyRSJK6GCSSpC4GiSSpi0EiSepikEiSuvw/wbNh8+Zgq8AAAAAASUVORK5CYII=\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "sns.countplot(y)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## STEP 4: DATA PRE-PROCESSING"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [],
   "source": [
    "# splitting the data\n",
    "x=data.iloc[:,1:]\n",
    "y=data['activity']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.preprocessing import StandardScaler"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [],
   "source": [
    " x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [],
   "source": [
    "scaler=StandardScaler()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [],
   "source": [
    "x_train=scaler.fit_transform(x_train)\n",
    "x_test=scaler.transform(x_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(70870, 6)"
      ]
     },
     "execution_count": 24,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "x_train.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [],
   "source": [
    "x_train=x_train.reshape(-1,1,6)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [],
   "source": [
    "x_test=x_test.reshape(-1,1,6)"
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
       "(70870, 1, 6)"
      ]
     },
     "execution_count": 27,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "x_train.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(17718, 1, 6)"
      ]
     },
     "execution_count": 28,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "x_test.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#  STEP 5: BUILDING THE MODEL"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [],
   "source": [
    "model=Sequential()\n",
    "model.add(LSTM(units=100,input_shape=(1,6),return_sequences=True))\n",
    "model.add(LSTM(units=100,input_shape=(1,6),return_sequences=True))\n",
    "model.add(Dropout(0.2))\n",
    "model.add(Dense(units=2,activation='softmax'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [],
   "source": [
    "model.compile(loss='sparse_categorical_crossentropy',\n",
    "             metrics='accuracy',\n",
    "             optimizer='adam')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Epoch 1/20\n",
      "1772/1772 [==============================] - 19s 8ms/step - loss: 0.1079 - accuracy: 0.9623 - val_loss: 0.0605 - val_accuracy: 0.9781\n",
      "Epoch 2/20\n",
      "1772/1772 [==============================] - 15s 8ms/step - loss: 0.0587 - accuracy: 0.9799 - val_loss: 0.0511 - val_accuracy: 0.9814\n",
      "Epoch 3/20\n",
      "1772/1772 [==============================] - 13s 8ms/step - loss: 0.0517 - accuracy: 0.9833 - val_loss: 0.0450 - val_accuracy: 0.9848\n",
      "Epoch 4/20\n",
      "1772/1772 [==============================] - 14s 8ms/step - loss: 0.0454 - accuracy: 0.9860 - val_loss: 0.0393 - val_accuracy: 0.9870\n",
      "Epoch 5/20\n",
      "1772/1772 [==============================] - 14s 8ms/step - loss: 0.0407 - accuracy: 0.9866 - val_loss: 0.0392 - val_accuracy: 0.9868\n",
      "Epoch 6/20\n",
      "1772/1772 [==============================] - 13s 7ms/step - loss: 0.0376 - accuracy: 0.9875 - val_loss: 0.0333 - val_accuracy: 0.9885\n",
      "Epoch 7/20\n",
      "1772/1772 [==============================] - 14s 8ms/step - loss: 0.0347 - accuracy: 0.9883 - val_loss: 0.0321 - val_accuracy: 0.9890\n",
      "Epoch 8/20\n",
      "1772/1772 [==============================] - 12s 7ms/step - loss: 0.0326 - accuracy: 0.9887 - val_loss: 0.0298 - val_accuracy: 0.9894\n",
      "Epoch 9/20\n",
      "1772/1772 [==============================] - 12s 7ms/step - loss: 0.0314 - accuracy: 0.9894 - val_loss: 0.0283 - val_accuracy: 0.9893\n",
      "Epoch 10/20\n",
      "1772/1772 [==============================] - 13s 8ms/step - loss: 0.0294 - accuracy: 0.9901 - val_loss: 0.0293 - val_accuracy: 0.9898\n",
      "Epoch 11/20\n",
      "1772/1772 [==============================] - 13s 8ms/step - loss: 0.0284 - accuracy: 0.9903 - val_loss: 0.0288 - val_accuracy: 0.9894\n",
      "Epoch 12/20\n",
      "1772/1772 [==============================] - 15s 9ms/step - loss: 0.0278 - accuracy: 0.9903 - val_loss: 0.0269 - val_accuracy: 0.9904\n",
      "Epoch 13/20\n",
      "1772/1772 [==============================] - 14s 8ms/step - loss: 0.0267 - accuracy: 0.9909 - val_loss: 0.0327 - val_accuracy: 0.9883\n",
      "Epoch 14/20\n",
      "1772/1772 [==============================] - 12s 7ms/step - loss: 0.0260 - accuracy: 0.9911 - val_loss: 0.0287 - val_accuracy: 0.9898\n",
      "Epoch 15/20\n",
      "1772/1772 [==============================] - 13s 7ms/step - loss: 0.0258 - accuracy: 0.9913 - val_loss: 0.0247 - val_accuracy: 0.9911\n",
      "Epoch 16/20\n",
      "1772/1772 [==============================] - 13s 8ms/step - loss: 0.0252 - accuracy: 0.9911 - val_loss: 0.0255 - val_accuracy: 0.9905\n",
      "Epoch 17/20\n",
      "1772/1772 [==============================] - 12s 7ms/step - loss: 0.0245 - accuracy: 0.9914 - val_loss: 0.0247 - val_accuracy: 0.9910\n",
      "Epoch 18/20\n",
      "1772/1772 [==============================] - 12s 7ms/step - loss: 0.0241 - accuracy: 0.9918 - val_loss: 0.0257 - val_accuracy: 0.9905\n",
      "Epoch 19/20\n",
      "1772/1772 [==============================] - 13s 7ms/step - loss: 0.0235 - accuracy: 0.9916 - val_loss: 0.0244 - val_accuracy: 0.9910\n",
      "Epoch 20/20\n",
      "1772/1772 [==============================] - 13s 7ms/step - loss: 0.0228 - accuracy: 0.9918 - val_loss: 0.0251 - val_accuracy: 0.9910\n"
     ]
    }
   ],
   "source": [
    "history=model.fit(x_train,y_train,epochs=20,validation_split=0.2,batch_size=32)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.plot(history.history['accuracy'], label='accuracy')\n",
    "plt.plot(history.history['val_accuracy'], label= 'val_accuracy')\n",
    "plt.title('model accuracy')\n",
    "plt.xlabel('epoch')\n",
    "plt.ylabel('accuracy')\n",
    "plt.legend(loc='lower right')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.plot(history.history['loss'], label='loss',color='k')\n",
    "plt.plot(history.history['val_loss'], label= 'val_loss',color='r')\n",
    "plt.title('model accuracy')\n",
    "plt.xlabel('epoch')\n",
    "plt.ylabel('accuracy')\n",
    "plt.legend(loc='lower right')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# STEP 6: SAVING THE MODEL"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "metadata": {},
   "outputs": [],
   "source": [
    "model.save('walk_run_model.h5')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# STEP 7: LOADING AND TESTING THE MODEL"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "metadata": {},
   "outputs": [],
   "source": [
    "loaded_model=load_model('walk_run_model.h5')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "metadata": {},
   "outputs": [],
   "source": [
    "predictions=loaded_model.predict(x_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 51,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([[[3.0321027e-05, 9.9996972e-01]],\n",
       "\n",
       "       [[1.6870159e-10, 1.0000000e+00]],\n",
       "\n",
       "       [[1.0166847e-05, 9.9998987e-01]],\n",
       "\n",
       "       ...,\n",
       "\n",
       "       [[1.3452052e-12, 1.0000000e+00]],\n",
       "\n",
       "       [[3.1906322e-05, 9.9996805e-01]],\n",
       "\n",
       "       [[2.9208445e-11, 1.0000000e+00]]], dtype=float32)"
      ]
     },
     "execution_count": 51,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "predictions"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([0.9999697 , 1.        , 0.99998987, ..., 1.        , 0.99996805,\n",
       "       1.        ], dtype=float32)"
      ]
     },
     "execution_count": 57,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "predictions[:,0,1]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 58,
   "metadata": {},
   "outputs": [],
   "source": [
    "y_pred=np.where(predictions[:,0,1]>0.5,1,0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 59,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([1, 1, 1, ..., 1, 1, 1])"
      ]
     },
     "execution_count": 59,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "y_pred"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 61,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.991646912744102"
      ]
     },
     "execution_count": 61,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "accuracy_score(y_test,y_pred)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Project Analysis\n",
    "A better understanding of Recurrent neural networks(RNN) and Long short term memory(LSTM) networks was imperative for the execution of this project. Several articles and videos pertinent to the same was explored for achieving this. We understood that an LSTM network is a type of RNN, which is capable of learning order dependence especially in sequence prediction problems. They use information from previous steps along with new information to carry out the predictions.\n",
    "\n",
    "The dataset given comprises of accelerometer and gyroscope readings for each of the sensor's axes, thus making a total of 6 independent variables or predictors. \n",
    "\n",
    "The pairplot function from seaborn was used inorder to visualize the realationship between each of the predictors so as to detect any kind of correlation between them, which in this case, was absent.Then, boxplots where used to detect the outliers in the data. Even though there were several points outside the inter-quartile range, they were clustered together and were not taken as outliers. However, the isolated points at the extremities were eliminated and imputed with the mean value. Skewness was checked using the histplot function from matplotlib. It was observed that most of the features are almost normally distributed.Applying log, square root or cube root transformations were unsuccessful as skewness of one or more features increased as the others decreased. So the skewness was left as such. The count plot showed an equillibrium of the values of target variable in the given dataset. Feature importances were measured by utilizing the XGBclassifier from xgboost and 'accelerometer_y' and 'gyro_y' had the maximum and minimum values respectively. \n",
    "\n",
    "Data pre-processing involved eliminating redundant variables('username','date','time','wrist') and splitting the predictor and target variable into x and y respectively.This was further split into training and testing dataset for model training and evaluation. The data was normalized using the StandardScaler package from scikit learn inorder to reduce the computational complexity.\n",
    "\n",
    "Model was built using the Sequential,LSTM,Dropout and Dense functions from the keras API. Two LSTM layers, each with 100 units one dropout layer with a rate of 0.2 to prevent overfitting and one Dense layer using 'softmax' activation for classification was used to build the model.Model was compiled with sparse categorical cross entropy as the loss function, accuracy as the evaluation metric and Adam as the optimizer. After running the model upto 20 epochs at a batch size of 32 and a validation split of 20% using the training data, a validation accuracy of 99.1% was achieved.This was followed by saving the model, loading it and then tesing it using the test data, where we achieved an accuracy of ~99.165%."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
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
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}