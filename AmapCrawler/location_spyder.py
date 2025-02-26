{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "* [PEP 465 -- A dedicated infix operator for matrix multiplication](https://www.python.org/dev/peps/pep-0465/)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "%reload_ext autoreload\n",
    "%autoreload 2\n",
    "%matplotlib inline\n",
    "\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "import sys\n",
    "sys.path.append('..')\n",
    "\n",
    "from helper import linear_regression as lr  # my own module\n",
    "from helper import general as general"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>population</th>\n",
       "      <th>profit</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>6.1101</td>\n",
       "      <td>17.5920</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>5.5277</td>\n",
       "      <td>9.1302</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>8.5186</td>\n",
       "      <td>13.6620</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>7.0032</td>\n",
       "      <td>11.8540</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5.8598</td>\n",
       "      <td>6.8233</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   population   profit\n",
       "0      6.1101  17.5920\n",
       "1      5.5277   9.1302\n",
       "2      8.5186  13.6620\n",
       "3      7.0032  11.8540\n",
       "4      5.8598   6.8233"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data = pd.read_csv('ex1data1.txt', names=['population', 'profit'])\n",
    "\n",
    "data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# compute cost\n",
    "<img style=\"float: left;\" src=\"../img/linear_cost.png\">"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(97, 2) <class 'numpy.ndarray'>\n",
      "(97,) <class 'numpy.ndarray'>\n"
     ]
    }
   ],
   "source": [
    "X = general.get_X(data)\n",
    "print(X.shape, type(X))\n",
    "\n",
    "y = general.get_y(data)\n",
    "print(y.shape, type(y))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "theta = np.zeros(X.shape[1])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "32.072733877455676"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "lr.cost(theta, X, y)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# batch gradient decent\n",
    "<img style=\"float: left;\" src=\"../img/linear_gradient.png\">"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "epoch = 500\n",
    "final_theta, cost_data = lr.batch_gradient_decent(theta, X, y, epoch)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "4.7138095311168664"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# compute final cost\n",
    "lr.cost(final_theta, X, y)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# visualize cost data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.text.Text at 0x1182d8f98>"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAArkAAAHxCAYAAABpvaQoAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz\nAAAPYQAAD2EBqD+naQAAIABJREFUeJzt3Xt0lOWBx/HfXMiEWwqEcJFqRagNFyGRW3FFNAewu4ui\nFV3tiopiqghsRVTwskCliqAoCGYrsqlFYTmCeO+xBT2giAIRJAocTUAgFZFQMIJJJjPz7h/JvJnh\nUkmY5B3e5/s5J2cy77x554Gnod88PjPxWJZlCQAAAHARr9MDAAAAABKNyAUAAIDrELkAAABwHSIX\nAAAArkPkAgAAwHWIXAAAALgOkQsAAADXIXIBAADgOkQuAAAAXCcpInfPnj267bbblJ2drZycHC1a\ntMh+bMaMGcrMzFS3bt3s25deesnB0QIAACDZ+Z0egGVZys3NVe/evfXaa6/pq6++0sSJE9WhQwf9\n+7//u3bu3KlJkybp6quvtr+mRYsWDo4YAAAAyc7xldzS0lJ1795dU6dO1TnnnKNLLrlEAwcOVEFB\ngSSpuLhY3bt3V3p6uv0RCAQcHjUAAACSmeORm5GRoTlz5qhZs2aSpIKCAm3cuFEDBgzQkSNHtH//\nfp177rnODhIAAABnFMe3K8TKycnRvn37dOmll2rYsGHaunWrPB6P8vLytHbtWrVq1UqjR4/WVVdd\n5fRQAQAAkMSSKnKfeeYZlZaWaurUqfrDH/6gnj17yuv1qkuXLho1apQ2bNighx9+WC1atNCQIUOc\nHi4AAACSlMeyLMvpQRzrnXfe0b333quCggKVl5crLS3NfmzGjBnatWtX3Dsw/DOWZcnj8TTUUAEA\nAJCEHF/JPXjwoDZv3hy3Mtu1a1dVVVXp6NGjatWqVdz55513nj7++ONTvr7H41FZWbnC4UjCxozk\n5PN5lZbWlPk2BPNtFubbLMy3WaLznWiOR25JSYnGjx+vtWvXKiMjQ5JUWFioNm3a6M9//rM2b96s\n/Px8+/zt27erc+fOdXqOcDiiUIhvElMw32Zhvs3CfJuF+cbpcPzdFS644AL17NlTU6ZMUXFxsdas\nWaMnnnhCd955py677DJt3LhR+fn52rt3r5YsWaLXX39dY8aMcXrYAAAASGJJsSf3wIEDeuSRR7R+\n/Xo1bdpUN954o3JzcyVJ7777rubOnavdu3erU6dOuvvuu+v8orNDh47yk6AB/H6vWrduznwbgvk2\nC/NtFubbLNH5TrSkiNyGxjeJGfhH0SzMt1mYb7Mw32ZpqMh1fLsCAAAAkGhELgAAAFyHyAUAAIDr\nELkAAABwHSIXAAAArkPkAgAAwHWIXAAAALgOkQsAAADXIXIBAADgOkQuAAAAXIfIBQAAgOsQuQAA\nAHAdIhcAAACuQ+QCAADAdYhcAAAAuA6RCwAAANchcgEAAOA6RC4AAABch8gFAACA6xC5AAAAcB0i\nFwAAAK5D5AIAAMB1iFwAAAC4DpELAAAA1yFyAQAA4DpELgAAAFyHyAUAAIDrELkAAABwHddH7vtb\n/q6IZTk9DAAAADQi10furMWb9PnOfzg9DAAAADQi10euJP2jrMLpIQAAAKARGRG5bFYAAAAwixmR\nS+UCAAAYxYjIZS0XAADALEZELiu5AAAAZjEicgEAAGAWIyKXhVwAAACzmBG57FcAAAAwihGRCwAA\nALMYEbks5AIAAJjFjMhlVy4AAIBRjIhcGhcAAMAsRkQujQsAAGAWMyKXygUAADCKEZHLWi4AAIBZ\njIhcVnIBAADMYkTkAgAAwCxGRC4ruQAAAGYxI3LZkwsAAGCUpIjcPXv26LbbblN2drZycnK0aNEi\n+7GSkhKNHj1a2dnZGj58uNatW1f3J6BxAQAAjOJ45FqWpdzcXLVt21avvfaapk2bpry8PL311luS\npLFjx6pdu3ZasWKFrrzySo0bN07ffPNN3Z6jIQYOAACApOV3egClpaXq3r27pk6dqmbNmumcc87R\nwIEDVVBQoPT0dJWUlOjll19WIBBQbm6u1q9fr+XLl2vcuHGn/BzsyQUAADCL4yu5GRkZmjNnjpo1\nayZJKigo0KZNm9S/f399+umn6tGjhwKBgH1+nz59tGXLljo+C5ULAABgEscjN1ZOTo5uvPFGZWVl\nadiwYTpw4IDatWsXd056err2799fp+uykgsAAGAWx7crxHrmmWdUWlqqadOm6dFHH1V5eblSUlLi\nzklJSVEwGKzTdT0ej/z+pOp5NACfzxt3C3djvs3CfJuF+TZLQ81zUkVujx49JEmTJ0/WpEmTNHLk\nSJWVlcWdEwwGlZqaWqfrBgJ+tW7dPGHjRHJLS2vq9BDQiJhvszDfZmG+cTocj9yDBw9q8+bNGjJk\niH2sa9euqqqqUkZGhoqLi+POLy0tVUZGRp2eo6KiSocOHU3IeJG8fD6v0tKaqqysXOFwxOnhoIEx\n32Zhvs3CfJslOt+J5njklpSUaPz48Vq7dq0dr4WFhUpPT1efPn20aNEiBYNBe9tCQUGB+vbtW6fn\nCEcshUJ8k5giHI4w3wZhvs3CfJuF+cbpcHyzywUXXKCePXtqypQpKi4u1po1a/TEE0/ozjvvVL9+\n/dSxY0dNnjxZRUVFeu6551RYWKiRI0fW6TksXnkGAABgFMcj1+v16tlnn1WzZs10/fXX6+GHH9ZN\nN92kG2+8UV6vV3l5eTpw4ICuueYavfHGG1qwYIE6dOjg9LABAACQxBzfriBVv1fuvHnzTvjY2Wef\nrcWLF5/W9VnIBQAAMIvjK7mNgcYFAAAwixGRy1IuAACAWYyIXBoXAADALGZELhsWAAAAjGJI5AIA\nAMAkZkQu+xUAAACMYkTkspQLAABgFiMil5VcAAAAs5gRuU4PAAAAAI3KjMilcgEAAIxiSORSuQAA\nACYxInIBAABgFiMil5VcAAAAsxgSuU6PAAAAAI3JjMjl/RUAAACMYkbk0rgAAABGMSRyqVwAAACT\nGBG5AAAAMIsRkctCLgAAgFkMiVwqFwAAwCRGRC4AAADMYkTkspILAABgFjMi1+kBAAAAoFGZEblU\nLgAAgFEMiVwqFwAAwCRGRC4AAADMYkTkspILAABgFjMi1+kBAAAAoFEZEblULgAAgFmMiFy2KwAA\nAJjFjMh1egAAAABoVGZELpULAABgFEMil8oFAAAwiRmR6/QAAAAA0KjMiFxWcgEAAIxiROQCAADA\nLEZELgu5AAAAZjEictmVCwAAYBYjIpeVXAAAALOYEblODwAAAACNyojIpXIBAADMYkTk8hZiAAAA\nZjEjcp0eAAAAABqVEZELAAAAsxgRuWxXAAAAMIshkev0CAAAANCYzIhcduUCAAAYxYjIpXEBAADM\nYkTk0rgAAABmSYrI3b9/vyZMmKABAwZo8ODBmjlzpoLBoCRpxowZyszMVLdu3ezbl156qU7XZ08u\nAACAWfxOD0CSJkyYoFatWmnJkiU6fPiwHnjgAfl8Pt17773auXOnJk2apKuvvto+v0WLFnV8BioX\nAADAJI6v5O7cuVNbt27VY489pi5duqhPnz6aMGGC3nzzTUlScXGxunfvrvT0dPsjEAjU6TlYyQUA\nADCL45GbkZGhhQsXqk2bNvYxy7L0/fff68iRI9q/f7/OPffc03oOGhcAAMAsjkduy5YtdfHFF9v3\nLcvSiy++qIsuukg7d+6Ux+NRXl6eBg8erBEjRujVV1+t83PwyyAAAADMkhR7cmPNmjVLO3bs0PLl\ny/XZZ5/J6/WqS5cuGjVqlDZs2KCHH35YLVq00JAhQ075mh555Pc73vNoYD6fN+4W7sZ8m4X5Ngvz\nbZaGmuekitzZs2dr8eLFevrpp9W1a1d17dpVOTk5SktLkySdf/75+uqrr7R06dI6Ra7X51Xr1s0b\nathIMmlpTZ0eAhoR820W5tsszDdOR9JE7iOPPKJly5Zp9uzZcQEbDdyo8847Tx9//HGdrh0KhXXo\n0NGEjBPJy+fzKi2tqcrKyhUOR5weDhoY820W5tsszLdZovOdaEkRufPnz9eyZcv01FNPaejQofbx\nefPmafPmzcrPz7ePbd++XZ07d67T9S3LUijEN4kpwuEI820Q5tsszLdZmG+cDsc3uxQXFysvL0+5\nubnKzs5WaWmp/XHZZZdp48aNys/P1969e7VkyRK9/vrrGjNmTJ2eg9edAQAAmMXxldzVq1crEoko\nLy9PeXl5kqpXXj0ej7Zv36558+Zp7ty5mjt3rjp16qQnn3xSvXr1cnjUAAAASGaOR25ubq5yc3NP\n+nhOTo5ycnJO6zl4CzEAAACzOL5doTGQuAAAAGYxInIBAABgFiMil90KAAAAZjEicgEAAGAWIyKX\nF54BAACYxYzIdXoAAAAAaFRGRC6VCwAAYBYjIjfCdgUAAACjGBG5AAAAMIsRkctCLgAAgFmMiFwA\nAACYxYjItXjlGQAAgFGMiFwaFwAAwCxGRC6NCwAAYBYzIpfKBQAAMIoRkctaLgAAgFmMiFwSFwAA\nwCxGRC6VCwAAYBYjIpfGBQAAMIsZkUvlAgAAGMWIyGUtFwAAwCxGRC4ruQAAAGYxInIBAABgFiMi\nl5VcAAAAsxgRuQAAADCLEZFr8cIzAAAAo5gRuTQuAACAUYyIXAAAAJjFiMhlJRcAAMAsRkQuAAAA\nzGJE5PLCMwAAALMYEbk0LgAAgFmMiFwaFwAAwCxGRC6VCwAAYBYjIpfGBQAAMIsRkQsAAACzGBG5\nFm+UCwAAYBQjIhcAAABmMSJyWcgFAAAwixGRCwAAALMYEbks5AIAAJjFjMilcgEAAIxiROQCAADA\nLEZELm8hBgAAYBYjIhcAAABmMSJyWccFAAAwixGRS+UCAACYxYjIpXEBAADMYkTkAgAAwCyOR+7+\n/fs1YcIEDRgwQIMHD9bMmTMVDAYlSSUlJRo9erSys7M1fPhwrVu3rl7PwZsrAAAAmMXxyJ0wYYIq\nKyu1ZMkSzZkzR++9957mzp0rSRo7dqzatWunFStW6Morr9S4ceP0zTffODxiAAAAJDu/k0++c+dO\nbd26VevWrVObNm0kVUfvrFmzNGjQIJWUlOjll19WIBBQbm6u1q9fr+XLl2vcuHF1eh4WcgEAAMzi\n6EpuRkaGFi5caAdu1Pfff69PP/1UPXr0UCAQsI/36dNHW7ZsqfsTsV8BAADAKI5GbsuWLXXxxRfb\n9y3L0osvvqiBAwfqwIEDateuXdz56enp2r9/f52fh8QFAAAwi6PbFY41a9Ysbd++XcuXL1d+fr5S\nUlLiHk9JSbFflFZXfr/j24/RwHw+b9wt3I35NgvzbRbm2ywNNc9JE7mzZ8/W4sWL9fTTT6tr164K\nBAL67rvv4s4JBoNKTU2t1/Vbt26eiGHiDJCW1tTpIaARMd9mYb7NwnzjdCRF5D7yyCNatmyZZs+e\nrSFDhkiS2rdvr6KiorjzSktLlZGRUefrW5Z06NDRhIwVycvn8yotranKysoVDkecHg4aGPNtFubb\nLMy3WaLznWiOR+78+fO1bNkyPfXUUxo6dKh9vHfv3lq4cKGCwaC9baGgoEB9+/at83NYkkIhvklM\nEQ5HmG+DMN9mYb7NwnzjdDi62aW4uFh5eXnKzc1Vdna2SktL7Y/+/furY8eOmjx5soqKivTcc8+p\nsLBQI0eOrPsT8cozAAAAozi6krt69WpFIhHl5eUpLy9PUvU7LHg8Hm3fvl0LFizQgw8+qGuuuUbn\nnHOOFixYoA4dOtT5eWhcAAAAszgaubm5ucrNzT3p4+ecc44WL17ciCMCAACAG/DeHAAAAHAdYyLX\n4reeAQAAGMOcyHV6AAAAAGg0xkQulQsAAGAOYyLXonIBAACMYU7k0rgAAADGMCZyAQAAYA5jIpeV\nXAAAAHMYE7m88gwAAMAcxkQuK7kAAADmMCdynR4AAAAAGo0xkUvlAgAAmMOYyOV9cgEAAMxRr8i9\n6aabVFZWdtzxgwcP6qqrrjrtQTUE9uQCAACYw3+qJ65Zs0aFhYWSpI0bN+p//ud/1KxZs7hzdu/e\nrb///e+JHSEAAABQR6ccuZ06ddLvf/97WTVLom+//ba83tqFYI/Ho2bNmum+++5L/CgTgJVcAAAA\nc5xy5Hbt2lWrV6+WJOXk5Gj58uVq06ZNgw0s8ahcAAAAU9RrT+67774bF7hVVVUqLCzU0aNHEzaw\nRCNxAQAAzFGvyN23b59uvfVWbd26VRUVFbrqqqt07bXXKicnR9u3b0/0GBOC7QoAAADmqFfkPvbY\nY/r+++/Vpk0b/eUvf9G+ffu0ZMkSDR06VLNnz070GBPConIBAACMccp7cmN99NFHeuGFF/TTn/5U\nTzzxhAYNGqQLL7xQrVu31q9//etEjzEhSFwAAABz1Gslt6qqSj/5yU9kWZbWr1+viy66SJIUiUTk\n99ermxselQsAAGCMehVp9+7dtXz5cmVkZKisrEyDBw9WMBjUwoULlZmZmegxJgSNCwAAYI56Re79\n99+vO+64Q4cOHdLtt9+uDh06aNq0aVq9erWef/75RI8xMdiTCwAAYIx6RW6vXr30wQcf6MiRI0pL\nS5Mk3Xzzzfrd736nVq1aJXSAiULiAgAAmKPeG2g9Ho+2bNmiL774Qn6/X127dtU555yTyLElFAu5\nAAAA5qhX5B4+fFi33XabPv/8c6WlpSkSiejIkSPq0aOH8vPz7dVdAAAAwAn1eneFxx9/XBUVFXr1\n1Ve1YcMGbdq0Sa+++qqCwaCefPLJRI8xIXifXAAAAHPUK3Lfe+89TZ06Ne6dFDIzM/XQQw9p1apV\nCRscAAAAUB/1itxQKKS2bdsed7xt27Y6cuTIaQ+qIbCQCwAAYI56RW6PHj20dOnS444vXbpU3bp1\nO+1BNQSL91cAAAAwRr1eePa73/1ON910k7Zs2aILL7xQHo9HmzZt0o4dO5L4fXKdHgAAAAAaS70i\nNzs7Wy+99JKef/55ffDBB7IsS7t379bSpUvVq1evRI8xIWhcAAAAc9Rru8Lnn3+u22+/XZ06ddJb\nb72lt99+W+3bt9fYsWP15ZdfJnqMCUHkAgAAmKNekTtz5kzl5OTo7rvvto/97W9/06BBg/TYY48l\nbHAJxSvPAAAAjFGvyP3ss880duxYpaSk2Md8Pp9yc3P16aefJmxwiUTiAgAAmKNekdu8eXPt3bv3\nuOPffvttXPgmFSoXAADAGPWK3Msvv1zTp0/X+vXrdfToUR09elQfffSRpk+frqFDhyZ6jAlB4wIA\nAJijXu+ucM8992jPnj0aPXq0PB6PfXzo0KG67777Eja4ROLX+gIAAJijXpHbrFkzLVy4ULt27dIX\nX3whv9+vLl266Nxzz03w8AAAAIC6q1fkRnXu3FmdO3dO1FgaFAu5AAAA5qjXntwzEY0LAABgDmMi\nl6VcAAAAcxgTuSQuAACAOYyJXCoXAADAHMZELo0LAABgDnMilz25AAAAxjAmcgEAAGAOYyKXhVwA\nAABzJFXkBoNBXXHFFdq4caN9bMaMGcrMzFS3bt3s25deesnBUQIAACDZndZvPEukYDCoiRMnqqio\nKO74zp07NWnSJF199dX2sRYtWtT5+hYvPQMAADBGUqzkFhcX67rrrlNJSckJH+vevbvS09Ptj0Ag\nUOfnYLsCAACAOZIicjds2KCBAwdq2bJlce+CcOTIEe3fv1/nnnuuc4MDAADAGScptivccMMNJzy+\nc+dOeTwe5eXlae3atWrVqpVGjx6tq666qs7PwUouAACAOZIick9m586d8nq96tKli0aNGqUNGzbo\n4YcfVosWLTRkyJA6Xcvr9cjvT4qFazQQn88bdwt3Y77Nwnybhfk2S0PNc1JH7lVXXaWcnBylpaVJ\nks4//3x99dVXWrp0aZ0jt2XLVLVu3bwhhokkk5bW1OkhoBEx32Zhvs3CfON0JHXkSrIDN+q8887T\nxx9/XOfrlJWV69Cho4kaFpKQz+dVWlpTlZWVKxyOOD0cNDDm2yzMt1mYb7NE5zvRkjpy582bp82b\nNys/P98+tn37dnXu3LnO1wqFIwqF+EYxQZi5NgrzbRbm2yzMN05HUm92ueyyy7Rx40bl5+dr7969\nWrJkiV5//XWNGTOmztfihWcAAADmSLrI9Xg89ucXXHCB5s2bp1dffVVXXHGFXnrpJT355JPq1auX\ngyMEAABAsku67Qrbt2+Pu5+Tk6OcnJzTvq7FUi4AAIAxkm4lFwAAADhdxkQuC7kAAADmMCdynR4A\nAAAAGo0xkctSLgAAgDmMiVwSFwAAwBxELgAAAFzHmMilcgEAAMxhTORaVC4AAIAxjIlcGhcAAMAc\nxkQujQsAAGAOcyKXygUAADCGMZHLWi4AAIA5jIlcVnIBAADMYU7kOj0AAAAANBpjIpfKBQAAMIcx\nkcv75AIAAJjDmMilcQEAAMxhTOTSuAAAAOYwJ3KpXAAAAGMYE7ms5QIAAJjDmMhlJRcAAMAcxkQu\nAAAAzGFM5LKQCwAAYA5zIpf9CgAAAMYwJnIBAABgDmMil4VcAAAAc5gTuezKBQAAMIYxkUvjAgAA\nmMOYyKVxAQAAzGFM5FK5AAAA5jAmciO88gwAAMAYxkQuAAAAzGFM5LKQCwAAYA5zIpdNuQAAAMYw\nJnJpXAAAAHMYE7k0LgAAgDmMiVwAAACYw5jItXjlGQAAgDHMiVynBwAAAIBGY0zkUrkAAADmMCZy\naVwAAABzGBO5/DYIAAAAcxgTuSQuAACAOcyJXCoXAADAGMZELgAAAMxhTOTyPrkAAADmMCdynR4A\nAAAAGo0xkUvlAgAAmCOpIjcYDOqKK67Qxo0b7WMlJSUaPXq0srOzNXz4cK1bt65e16ZxAQAAzJE0\nkRsMBjVx4kQVFRXFHb/rrrvUrl07rVixQldeeaXGjRunb7755pSv6/HUfMKeXAAAAGMkReQWFxfr\nuuuuU0lJSdzx9evXa+/evfr973+v8847T7m5ucrKytLy5ctP+dp24yZwvAAAAEhuSRG5GzZs0MCB\nA7Vs2bK4d0HYunWrevTooUAgYB/r06ePtmzZcuoXr1nKZSEXAADAHH6nByBJN9xwwwmPHzhwQO3a\ntYs7lp6erv3795/ytT0/fgoAAABcJilWck+mvLxcKSkpccdSUlIUDAZP+RrRPbkWGxYAAACMkRQr\nuScTCAT03XffxR0LBoNKTU2tw1U8kix5PR75/Und9DhNPp837hbuxnybhfk2C/Ntloaa56SO3Pbt\n2x/3bgulpaXKyMg45WtEV3JTm6aodevmiRweklRaWlOnh4BGxHybhfk2C/ON05HUkdu7d28tXLhQ\nwWDQ3rZQUFCgvn37nvI1ontyf/ghqEOHjjbAKJEsfD6v0tKaqqysXOFwxOnhoIEx32Zhvs3CfJsl\nOt+JltSR279/f3Xs2FGTJ0/W2LFj9e6776qwsFAzZ8489YvULOVGIhGFQnyjmCAcZq5Nwnybhfk2\nC/ON05F0m108ntr3Q/B6vXr22Wd14MABXXPNNXrjjTe0YMECdejQoQ7Xq77lLcQAAADMkXQrudu3\nb4+7f/bZZ2vx4sX1vh6/DAIAAMA8SbeSm2j8Wl8AAADzuD5yo2u5JC4AAIA5XB+5HvYrAAAAGMf9\nkVtzS+MCAACYw/WRG13KtdiTCwAAYAzXR67nx08BAACAy7g/cmsqN8JCLgAAgDFcH7nsygUAADCP\n6yOX33gGAABgHtdHrpcXngEAABjH9ZHLK88AAADM4/rIjTZuhJVcAAAAY7g/cnndGQAAgHFcH7nR\ntVz25AIAAJjD9ZFrv7uCs8MAAABAI3J/5EY/oXIBAACM4frIFW8hBgAAYBzXRy7bFQAAAMzj/sit\nuWUlFwAAwByuj1x7u4LDwwAAAEDjcX3k8sIzAAAA87g/cqN7ctmuAAAAYAz3R67YrgAAAGAa10eu\nWMkFAAAwjusj1353BUdHAQAAgMbk/silcgEAAIzj+siNruWyXQEAAMAcro/c2ndXcHYcAAAAaDzm\nRC77FQAAAIzh+siN+XUQAAAAMITrI5ftCgAAAOZxf+TW3PLCMwAAAHO4P3I9/MYzAAAA07g+cm1U\nLgAAgDFcH7kpTar/iJVVYYdHAgAAgMbi+sjNaNVMklT6XbnDIwEAAEBjcX3ktmtTHbn/KKt0eCQA\nAABoLK6P3PY1kXu0MsKWBQAAAEMYE7mSVPpdhYMjAQAAQGNxfeS2a93U/vwg+3IBAACM4P7IZSUX\nAADAOK6P3NQUv9Kap0iSSg8TuQAAACZwfeRKUkarVEnSNwePODwSAAAANAa/0wNoDG1/0lTFfy/T\nluJ/6Mn/26zUFL9SU3zVtwFf7ecpPgWa+GqORc+p/dzvM+JnAgAAgDOeEZHb9ac/0cfb9kuSPv/q\nUL2v4/N6FGjiU6AmflOa+JR6kvv2eTH37XNiHg80IZ4BAAASzYjIHdbvbLVpGdCnRaX69h9HVBEM\nqyIYUmUwospQRMGqiEKRH79OOGLph8qQfqgMJXR8fp8nLnoDJwjhaEhHH48N59j7KX6fUpp4FWji\nUxO/Vx6PJ6FjBQAAOBMYEbkej0fZP89Q9s8zTnpOOBJRZTCsimBY5TURXBEM1xwLqTIYVmVVpPp4\nZUg/VFbZn1cEwwpWhVVRFVawKqJgKKKqkKWqsHVK4wuFLYXCIR2tSGw8eySlNKmO3hR/dQin+L1K\nqQnlaAynNKk+Hj0W97jfp5QUX/VtzPmBmvN8Xg8hDQAAko4RkXsqfF6vmqV61Sy1ScKuGYlYqqyq\nDeDqUA7bMV1ZFXs/pPLKkMorq2rCuTqsK2rOCYYiClZZqgqd2qqzJFmS/RxSVcL+XLG8Ho8CKTUR\nfWwkHxPUcZ/7qx9vEvt5zflN/N6a+7Xn+n3ENAAAOHVEbgPyej1qGvCracCvnyTwutF4tleQa4I5\nWFW92hysCqsyVL2qHD0ejefKqpAd20F75TmsqpClYChSvap8ihEtSRHLUnllWOWVDfsrkz2SHcTH\nR3D154EUr1o0D0gRS36v50cDOtCk5hoxsV37OFs9AAA4kyV95K5atUrjxo2Tx+ORZVnyeDwaNmyY\n5s6d6/RBb3S7AAAW2ElEQVTQHBMbzw0hYlm1ARy3khyN40h8VIfCMavP1bex5wZD0VtLVeHqrRyR\nU9vJYbOkmvHUocBPU2zwRrd0NPF71cRXc+v3yR93v/pz/3Hnnfi+33fyx3xeXowIAMDpSPrILSoq\nUk5OjmbMmCHLqi6jQCDg8Kjczevx1LxtWsM9RzgSUVXNi/6qV5KrP68K1URxKPp4zWOhiKpCNVs+\ngqGabRihmhivPT9iWaqoDFUHtb0ybSlcjzauqrmmE7weT0wMe+yoPlk4HxfWJzseDfGaGPf7PNWx\nHXOsic8jX80xr5fVbADAmSnpI7e4uFg///nP1aZNG6eHggTyeb3ypXgTGtJ+v1etWzfXoUNHFTom\nTiMRyw7oaDQfG9D2qnMooqqY+K7eNx0N6pB9flVVpGZluvq2+gWEVm1Yh+u+Ym2P17Ji9lM7x+vx\nyO/3qInPWxO+nphArgnwaCCfNJw98nu99qq33+exP/fFfv2pHmN/NgDgFJwRkfsv//IvTg8DZziv\n11P9NmspvkZ93nAkopC9TaMmjkO1cRyK+dz+iLtfvXodDIXsKK+KWemOu8YxoR2u5wp2rOqtK1aj\nbhM5FXZI17wo0ef12AHsi956a4M7+rjPVxPcJzgvet/vrTkv5utOeF7N47FfF3089vm8BDkAOCLp\nI3fXrl16//33lZeXp0gkol/96leaMGGCmjRJ3LsgAA2lesVaCqhx4zoqYlkKhSIKhY+P6OoYrr4f\nrtkrHQpHYo5Ft3zEBnq4NtRrbkP29aIfNdepWc2ODe5wpP6r27Gqn6P6RZfJrjqEExDdNbex1/N6\nPfJ7PXZs+7zxj5/w/nGfRz9irh/3OSvnAM5MSR25X3/9tSoqKhQIBDR37lyVlJRoxowZqqys1AMP\nPHDK1/HxG8WMEJ1n5jteShNnAvtkIpHauA4dE9vRVem4wD7JeeGIJZ/fp++PVqgyGFYoGt2RiB32\nseEdjt5GIjHhXR3i0QiPWKe/+n2s6PNIybUaXhc+r0femJg+LqxPGMdee5X9+OiOD25/zDW8cV9X\n+zVN/D61aB5QZWWVJMuO/Ojj3pPdek503Bt3zOMRIZ9k+PfcLA01zx4r+mquJFVWVqa0tDT7/l//\n+lfdd9992rx5M/8oAUg4y6qO0tpQjlnhrjkWDh8b6vHnnexYMBSu/rqq2BXxiELhsB34J/zacGyM\nx39EIpYikep3IEH9+X3VgR2/+n2iY/FxHQ3x2mM121RizznuWG3ke70xW19in8/nOekxr6c21r3e\n6u1Y1TFfez86Tq/n2PseexuN95j4j/2BAHCDpF7JlRQXuJLUpUsXVVZW6vDhw2rduvUpXaOsrFzh\nRC/PIOn4fF6lpTVlvg3RmPPtk+TzSoEUr6TkXFmKRCyFIpHaGA5Haleqrdr70dXs2miOxAf0sefZ\nq92RY+K/Js5jot++lr1dJfZaliLR68UEur2NpWYrS3RLS2Mvv4TClhRO/u0vjaU6gmsD+tgI9niq\nt2NFIzo2mmvP1wm+rvq6dqyf6OtqtuGkpjZRKBSWp2Y8Hnt1Xid4rtqtNV6v4p7T66ker/38Ned4\nVPtniV4n+nnsdaLP7fXE3I+7Xvy1PTF/bvs88V8L/pnov+eJltSR+8EHH+iee+7R2rVr7bcN27Zt\nm1q1anXKgSup+h9ch94KCo2P+TYL813LK4+8Po+a+CQl2TaVuopYNRFcE8ger9Qyran+8Y+jClaF\nawLZqr21Yle2j3nsmHOq3/nkROdE7PuhcMTeWhOOBnwkJtbDkWNiPfb5I/b2l9jr289pyY766K1l\nRc9PjlX5iGUpEpZ0ir+eHj/u2IC2g7tmu0xccMcdqw3sE36t95jrxB2LCXfvMdc59mu9HnnlkScu\n7uPPP9F1PLHPe+zYJfuc436I8NQ+5vd7ldP/3IT/nSd15GZnZ6tp06Z68MEHddddd2nPnj2aPXu2\nbr/9dqeHBgBoQF5PdbD7a1rd7/eqdctUKRR2/Q810Tg+UcBHAz32nNpYtuJvo4/VfL0VfcyqfucX\nKzbErejjtSvrlnXsDwPVK/XxPxBEasdqVQd+fNgrLvCtuLGdaOzVY7IsSR6PwjU/bFT/IBB9vPqH\nAiuJfig4FZYlhS1LkiXxHw2OY1zkNm/eXIsWLdKjjz6qkSNHqnnz5rr++ut16623Oj00AAAaRDTw\nHXpTlqTwz973/FhWTRTHBrkVs2puxcS/FRPRcccilizVRHPMDxFx5x93rDbSo19z3HVPeqz2h5jo\nWC0r/r8GVF87coJrHPuDwj8bd83fwYnGZP+QUHtb+3cR84OEdcznMX/nln3/9Od8165d6ty58+lf\nKEZSR65UvQd30aJFTg8DAAAkIfs/h6t25R+Nzzo24q1jj8VHf20oW/J4PercOSPhY0r6yAUAAEBy\ni/1ho678/oZ5QW9yvkwYAAAAOA1ELgAAAFyHyAUAAIDrELkAAABwHSIXAAAArkPkAgAAwHWIXAAA\nALgOkQsAAADXIXIBAADgOkQuAAAAXIfIBQAAgOsQuQAAAHAdIhcAAACuQ+QCAADAdYhcAAAAuA6R\nCwAAANchcgEAAOA6RC4AAABch8gFAACA6xC5AAAAcB0iFwAAAK5D5AIAAMB1iFwAAAC4DpELAAAA\n1yFyAQAA4DpELgAAAFyHyAUAAIDrELkAAABwHSIXAAAArkPkAgAAwHWIXAAAALgOkQsAAADXIXIB\nAADgOkQuAAAAXIfIBQAAgOsQuQAAAHAdIhcAAACuQ+QCAADAdYhcAAAAuA6RCwAAANchcgEAAOA6\nRC4AAABch8gFAACA6xC5AAAAcB0iFwAAAK5D5AIAAMB1iFwAAAC4DpELAAAA10n6yA0Gg3rggQfU\nr18/DRo0SPn5+U4PCQAAAEnO7/QAfszjjz+ubdu2afHixSopKdH999+vTp06adiwYU4PDQAAAEkq\nqVdyy8vLtXz5cj300EPKzMzUkCFDNGbMGL344otODw0AAABJLKkjd8eOHQqHw8rKyrKP9enTR1u3\nbnVwVAAAAEh2SR25Bw4cUKtWreT31+6qSE9PV2VlpQ4dOuTgyAAAAJDMknpPbnl5uVJSUuKORe8H\ng8FTvo7Pl9QtjwSJzjPzbQbm2yzMt1mYb7M01DwndeQGAoHjYjZ6v2nTpqd8nbS0Uz8XZz7m2yzM\nt1mYb7Mw3zgdSf0jUvv27XX48GFFIhH7WGlpqVJTU5WWlubgyAAAAJDMkjpyu3XrJr/fry1bttjH\nNm3apJ49ezo4KgAAACS7pI7c1NRUjRgxQlOnTlVhYaFWrVql/Px83XzzzU4PDQAAAEnMY1mW5fQg\n/pmKigpNnz5d77zzjlq2bKkxY8Zo1KhRTg8LAAAASSzpIxcAAACoq6TergAAAADUB5ELAAAA1yFy\nAQAA4DpELgAAAFyHyAUAAIDruDZyg8GgHnjgAfXr10+DBg1Sfn6+00NCAgSDQV1xxRXauHGjfayk\npESjR49Wdna2hg8frnXr1sV9zYcffqgrrrhCWVlZuuWWW7R3797GHjbqaP/+/ZowYYIGDBigwYMH\na+bMmfav9Ga+3WfPnj267bbblJ2drZycHC1atMh+jPl2t9zcXE2ZMsW+v23bNl133XXKysrStdde\nq88//zzu/DfffFNDhw5Vdna2xo0bp0OHDjX2kFFHq1atUmZmprp162bf/td//Zekhp9v10bu448/\nrm3btmnx4sWaOnWq5s+fr7/+9a9ODwunIRgMauLEiSoqKoo7ftddd6ldu3ZasWKFrrzySo0bN07f\nfPONJGnfvn266667dM0112jFihVq3bq17rrrLieGjzqYMGGCKisrtWTJEs2ZM0fvvfee5s6dK0ka\nO3Ys8+0ilmUpNzdXbdu21WuvvaZp06YpLy9Pb731liTm283eeustrV271r5fXl6u3Nxc9evXT6+8\n8oqysrL029/+VhUVFZKkrVu36qGHHtL48eO1bNkyfffdd3GBjORUVFSknJwcrVu3TuvWrdMHH3yg\nP/zhD40z35YL/fDDD1avXr2sjRs32seeffZZa9SoUQ6OCqejqKjIGjFihDVixAgrMzPT2rBhg2VZ\nlvXhhx9a2dnZVkVFhX3uLbfcYj3zzDOWZVnW008/HTfv5eXl1oUXXmh/PZJPcXGxlZmZaR08eNA+\n9uabb1qXXHKJtX79eubbZb799lvr7rvvto4ePWofGzdunDV9+nTm28UOHz5sDR482Lr22mutyZMn\nW5ZlWS+//LI1ZMiQuPOGDRtmrVy50rIsy7rvvvvscy3Lsvbt22dlZmZaJSUljTdw1NmkSZOsOXPm\nHHe8MebblSu5O3bsUDgcVlZWln2sT58+2rp1q4OjwunYsGGDBg4cqGXLlsmK+f0lW7duVY8ePRQI\nBOxjffr00ZYtW+zH+/XrZz+Wmpqq7t27a/PmzY03eNRJRkaGFi5cqDZt2sQd//777/Xpp58y3y6T\nkZGhOXPmqFmzZpKkgoICbdq0Sf3792e+Xezxxx/XiBEj1KVLF/vY1q1b1adPn7jzLrzwQns+t2zZ\nEjffHTp0UMeOHfXpp582zqBRL8XFxercufNxxxtjvl0ZuQcOHFCrVq3k9/vtY+np6aqsrGT/zhnq\nhhtu0P333x/3f3ZS9Vy3a9cu7lh6err2798vSfr222+Pe7xt27b240g+LVu21MUXX2zftyxLL774\nogYOHMh8u1xOTo5uvPFGZWVladiwYcy3S61fv14FBQXHbS050XzGzveJ/vfQtm1be/sKktOuXbv0\n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\nAABJRU5ErkJggg==\n",
      "text/plain": [
       "<matplotlib.figure.Figure at 0x118275eb8>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "ax = sns.tsplot(cost_data, time=np.arange(epoch+1))\n",
    "ax.set_xlabel('epoch')\n",
    "ax.set_ylabel('cost')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.legend.Legend at 0x1186c6780>"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAqEAAAHcCAYAAADm9nPcAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz\nAAAPYQAAD2EBqD+naQAAIABJREFUeJzs3Xlc1VXi//H3BWRxIVFRCzPNLBBNSLNssSRrrJ9WM60z\n0wZjNqnhVi6V05RmLqmJEYUCWVZj6cxUlk7T0Gp9LY2blZi5lEKJYJgbisD9/YEg6L0XLnzu+nk9\nH48ewud87udz4AC97zmfc47FZrPZBAAAAHhQkLcrAAAAAPMhhAIAAMDjCKEAAADwOEIoAAAAPI4Q\nCgAAAI8jhAIAAMDjCKEAAADwOEIoAAAAPI4QCgAAAI9zOYTu3LlTf/nLX5SYmKikpCRlZWXVlhUU\nFCg5OVmJiYkaNmyY1q5da2hlAQAAEBhcCqE2m00jR45Uhw4d9Oabb+rvf/+7MjIy9M4770iSRo0a\npY4dO2rlypW6/vrrNWbMGO3evdstFQcAAID/CnHl5JKSEvXq1UuPPfaYWrZsqa5du2rgwIHasGGD\n2rdvr4KCAr3xxhsKCwvTyJEj9fnnn2vFihUaM2aMu+oPAAAAP+RST2h0dLTmz5+vli1bSpI2bNig\n9evXa8CAAfr6668VHx+vsLCw2vP79esnq9VqbI0BAADg95o8MSkpKUl33HGHEhISdM0116i4uFgd\nO3asd0779u1VVFTU7EoCAAAgsDQ5hC5atEjPP/+8Nm/erJkzZ6qsrEyhoaH1zgkNDVV5eXmzKwkA\nAIDA0uQQGh8fryuuuEJTpkzR8uXL7QbO8vJyhYeHN/qaNputqdUBAACAH3FpYtLevXuVl5enIUOG\n1B4755xzdOzYMUVHR2vbtm31zi8pKVF0dHSjr2+xWLR/f5kqK6tcqRb8UHBwkCIjI2hvk6C9zYX2\nNhfa21xq2tsILoXQgoICPfDAA/r4449rw+U333yj9u3bq1+/fsrKylJ5eXntsPyGDRvUv39/lypU\nWVmligp+iM2C9jYX2ttcaG9zob3hKpeG4/v06aPevXtr6tSp2rZtmz766CM9/fTTuv/++3XhhRfq\n9NNP15QpU7R161ZlZmbqm2++0c033+yuugMAAMBPuRRCg4KC9Nxzz6lly5a6/fbbNW3aNN111126\n4447FBQUpIyMDBUXF+umm27S22+/rfT0dHXu3NlddQcAAICfsth8bDZQaekhuvNNICQkSFFRrWhv\nk6C9zYX2Nhfa21xq2tsITZ4dDwAAADQVIRQAAAAeRwgFAACAxxFCAQAA4HGEUAAAAHgcIRQAAAAe\nRwgFAACAxxFCAQAA4HEu7R0P191883AVFe2u/Tw4OFgxMV10ww036dZb/2jIPR544D5dcEF/JSff\nq5kzH5ckPfzwY05fU1FRodWrV2n48BtPuQYAAIC7EULdzGKxaNy4B5WUdLWk6vC3fv0XmjVrutq2\nbatrrrnW0PuNG/dgo87773/X6KWXcmpD6MyZT6tFixaG1gUAAMARhuM9oGXLVoqKaqeoqHaKju6o\na68dpv79L9KHH+a65V4tWza8ndbJu7W2adNG4eHhhtcHAADAHr/uCT18pEK//HrIo/c8vV0rtQxv\n/rctODhYLVq00AMP3KcePc7RZ599KpvNppdeWq4DB/Zr3rxZ2rDhS0VFtdd11w3TPfeMkMVikSR9\n9NEHev75RSopKdF11w1TVdWJvXpPHo7/z3/e1UsvZauoaLd69jxPEyZM0sGDB/XUU09IkgYNGqDX\nX39LTz75WL3h+HfffVuvvvqSfvnlZ519dg+NGTNeffsmSpJuueV6/elPd2nNmnf0ww9bdNZZZ2nq\n1L/p3HNjm/19AQAA5uC3IfTwkQpNyvhMh49WePS+LcNCNOf+S5ocRCsqKrR27cdav36dpk79m956\n6196991VWrAgXS1ahCgiIkKpqfepZ8/z9OKLr6mkpFhz5jypoKAg3X33X7Rjx3Y99thUjR49Thdd\nNFDLl7+ijRut6t9/wCn3Wrfuc82aNV3jx09Sv34X6o03/qHJkyfo9dffVGrqRP3jH8u0ZMnLOu20\n0+q97t1339aCBXP10ENTFRcXr3feeUsPPpiq1177pzp0iJYkZWdnavLkR9WtW3fNmjVdzzzztJ57\nbkmTvicAAMB8/DaE+pOnn35K8+fPkSSVlx9VeHi4brvtz7r66qF6661/6ZJLLlN8fG9J0oYNX6qo\nqEiZmUtlsVjUpcuZGj16nGbO/Lvuvvsvevfdt5WQcIFuueV2SdL48ZP02Wef2r3vW2/9U1dfPVTX\nX/97SdKYMeMUGtpCBw7sV+vWrRUUFKyoqKhTXrdixXLdeusfa59X/etfx8hq/UorV76u++4bLUm6\n7rrhuuyyQZKk22+/Q3/72xQDv2MAACDQ+W0IbRle3SPpD8PxI0bcr0GDrpQkhYWFqX37DrVD65J0\n+uln1H7844879Ntv+3TNNVfUHrPZqnTs2DHt379fP/20Qz17nldbFhISop49z7V73507f9KNN95c\n79xRo8Y2WN+fftqhlJSR9Y7Fx/fRTz/9WPt5ly5n1n7cqlUrVVR4tkcaAAD4N78NoVJ1EO1xxmkN\nn+hlbdu2VUxMF4floaGhtR9XVlbqrLO6adas+adMHmrVqnrC0cnHQ0Lsz2oPCWla84aGhtULyZJU\nVVWlqqrKZl8bAABAYna8z+na9SwVFe2uDa4xMV30888Fysp6QUFBQerevYc2b95Ue77NZtPWrVvs\nXqtLl67auvWH2s+rqqp0yy036NtvNzZYh5PP+e67b9S1a7emf2EAAAB1EEJ9zIABF6tz5zP0+OOP\navv2rfr66zzNmfOUIiIiZLFYdP31v9fmzZv08ss52rnzJz377IJ6i+HXdfPNt+m9997V6tWrVFhY\noLS0eZJsOvfcWEVEROjAgf0qKNilysrKeq+77bY/a+XK1/Wf/7yrXbt2KiNjkbZt+6F2TVEAAIDm\nYkzV7SzOS08a9g4KCtKsWfO0YMFc3XdfsiIiWiopaUjts5wxMV00a9Z8paXN09KlWbr88is1cOCl\ndq/dt2+iJk6cohdfXKJff92r886L0+zZCxQaGqoLLrhQMTFddPfdtysjI6tePZKShqi0dK+WLHlB\nv/5aop49z9OCBek688yujfqaAAAAGmKxnfyAoZeVlh5SRUVVwyfCr4WEBCkqqhXtbRK0t7nQ3uZC\ne5tLTXsbgeF4AAAAeBwhFAAAAB5HCAUAAIDHEUIBAADgcYRQAAAAeBwhFAAAAB5HCAUAAIDHEUIB\nAADgcYRQN5o583FdfvmFGjRogC6//MJ6/w0aNEBW61cuXzMvb4MGDRrQqHNXr16lW265weV7NEVe\n3gZdfvmFjT4/N/d9/frrr26sEQAA8GXsmORGhw8f0tGjRyVJ77//nv7xj2VasuRlSdXf8jZtIhUS\n4trOqRUVFTpwYL+ioto1eG55ebnKyg7rtNPaulx3V+XlbdDYsffr44+/aPDc3bt365Zbhis3N1cR\nEacFTHvDMXZUMRfa21xob3Mxcsck9o53o5YtW6lly+qGat26tYKCghUVFdWsa4aEhDQqgEpSaGio\nQkNDm3U/d7DZqurtVQ8AAMzHdCF006bv9eqrn6hNmzCNGHGd2rdv79X6zJz5uCRpy5bv9euve5WR\nkaXy8nItWrRA3367URUVFYqL66XJkx9R167dlJe3Qampf9Unn3yp3bt/0S23XK8ZM+bouecWqqSk\nWP36DdC0aU+oTZs2Wr16lbKzM/XGG28pL2+DZs58XH/+811aujRbBw8e0KBBgzV16t9qe2Pfe2+1\nsrJe0K+/7tVll10hm82ms87qpuTke0+p9+HDhzR79pP6/PO16tChg4YNu7Fe+caNVj3//LPasmWz\nLBaLEhIu0NSpf1O7du116603yGKx6KqrrtKjj/5d11xznV56KVtvv/2mSkr26LTT2uqGG/5g974A\nACAwmOqZ0CeeeFk33LBLmZmpmjfvTv3ud29pzZrPvF0t/ec/72rkyFGaM+cZnXFGjKZMmaCYmC5a\nuvQ1vfBCtqqqKpWRsaj2/JN7EZcty9Hjjz+lZ5/N1ObNm/SPfyyrU3ri3JKSYn34Ya7mz39WM2fO\n1Ucf5WrNmlWSpK+/tmrWrOm64457lJW1TOHhEcrN/a/DOs+ZM1O7du1UevpijR//kJYvP3HPQ4cO\natKk8Row4GItW7ZCCxakq7CwQC+//KIkafHipZKkFStWaMiQa7R69SqtWLFcU6dO02uv/UvJyfcq\nOztTP/zwfVO/pQAAwMeZJoRu2bJVr7wSrd9++72kYElttHNnqp5++itVVXn3GZa4uHhdcsllio2N\n09GjR3XjjTdrzJixOv30M9Sz53kaOnSYduzY7vD1f/nLXxUbG6e4uHhdffVQ5edvsnteZWWlxo+f\npO7dz9aFF16siy4aWHvuv/+9QldddY2GD79RXbuepQcfnKLo6I52r3Po0EF98MH7Gj/+IfXsea4u\nvPBi3XPPiV7Lo0ePKjl5hO65Z4Q6d+6s3r3P1xVXJGnHjm2SpLZtqx9JiIqKUmhoqDp3Pl1Tp/5N\nF1zQX507d9YNN/xB7dq1d/o1AwAA/2aa4fjXXvtQpaUPnHJ869YE7dixTT169PRCrap17nx67cfh\n4eG68cabtHr1Km3enK+ffvpRW7ZsVrt2Hey+1mKxqEuXM2s/b9WqlSorKxzeKyamS51zW6uiovrc\nbdt+0A033FRbFhwcrNjYOLvX2LVrp2w2m84559zaY3FxvWo/bteuvYYO/X9avvwV/fDDFv344w5t\n3bpF55+fYPd6iYn9tGnTt3rhhXT9+OMO/fDD9yot/VWVlZUOvw4AAODfTNMT2qFDG0mlpxxv2fJX\ntW4d6fkK1VF38lBZWZlGjLhT77//ns46q7tGjPirRo0a6/T1ISEt6n3ubMGDk2fj15wbHBysmln7\nJ8qc17vuferWobh4j+6663Z99dV6xcbGKTV1gm6//Q6H11m16t8aN260ysvLNXjwVVq4MEMdOkQ7\nvzkAAPBrpukJvfvu67RsWY62bZtU5+hRJSRsU6dO13utXifLy9ugvXv3atmyN2qf/Vy37jOdHBCN\n1r17D33//ebaz6uqqvTDD1vUs+e5p5zbtetZCgkJ0ebNm3TBBf0lSVu2nHjtxx9/qNNOO02zZy+o\nPfbGG/+oE1ot9QLsv//9TyUn36s//rE6qB44cEClpawhCgBAIDNNT2jr1m00b97F6t//SbVtu0Kd\nOr2oa66Zo+eeu8fbVasnMvI0lZUd1kcf5Wr37l/09tv/1j//+YbKy8vtnm/UMq9/+MOtev/997Rq\n1ZvaufMnLVz4tIqKfrG7lFLLlq30u99dp2eematNm77VV1+tV07O4try0047TUVFu7Vhw5f6+edC\nLVv2oj7++AMdO3ZMkhQRES5J2rx5s8rKyhQZeZrWr/9Cu3bt1ObN+XrssYdVWVnp8GsGAAD+zzQ9\noZJ0ySWJeuedBP3yy8+KiIho9HqbntS7dx8lJ9+r+fPnqLz8qHr06KmJE6do1qzp2ru35JTzjVpv\ns3fvPpowYZJychZr//7fNHjwEMXH93G4mP748ZO0YMFcTZgwRm3aROrmm29TevpCSVJS0tX6+mur\npk2bIotFio2N15gx45WV9YIqKip02mltNXTodRo3bpxGjx6rceMe1MyZjys5+U+KimqnpKSr1bJl\nBLPjAQAIYOyYBElSfv53atWqtbp2Pav22J133qo//ekuXXvtMMPvxw4b5kJ7mwvtbS60t7kYuWOS\naYbj4dy3336jSZPG6dtvN+rnnwv10kvZKi7eo4svvsTbVQMAAAHIVMPxcOwPf7hFu3f/rEcemaRD\nhw6qZ89z9fTTi3zykQUAAOD/GI6HVzB8Yy60t7nQ3uZCe5sLw/EAAADwa4RQAAAAeBwhFAAAAB5H\nCAUAAIDHEUIBAADgcYRQAAAAeJzLIbSoqEipqam66KKLdMUVV2jWrFm1e3zPmDFDsbGxiouLq/33\nlVdeMbzSAAAA8G8uL1afmpqqtm3b6tVXX9W+ffv08MMPKzg4WA899JC2b9+uBx98UL///e9rz2/d\n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\nagg7I7F8AAAAAElFTkSuQmCC\n",
      "text/plain": [
       "<matplotlib.figure.Figure at 0x11833b9b0>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "b = final_theta[0] # intercept\n",
    "m = final_theta[1] # slope\n",
    "\n",
    "plt.scatter(data.population, data.profit, label=\"Training data\")\n",
    "plt.plot(data.population, data.population*m + b, label=\"Prediction\")\n",
    "plt.legend(loc=2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "anaconda-cloud": {},
  "kernelspec": {
   "display_name": "Python [conda env:tf]",
   "language": "python",
   "name": "conda-env-tf-py"
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
   "version": "3.5.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 14:02:53 2018

@author: leshuangjiang
"""

import json
import time

import pandas as pd
import requests


class AmapCrwaler(object):
    def __init__(self):
        self.init_url = r'https://restapi.amap.com/v3/place/text?parameters'
        self.city_lst = "AMap_adcode.csv"
#        self.keywords = 'kikc'

    def spiders(self, keywords, city):
        '''构造请求函数'''
        one_city_pois = []
        payload = {
                'key': '38223614c364192a208aa2bc3d4b2e74',
                'keywords': keywords,
                'types': '060000',
                'city': city,
                'citylimit': 'true',
                'offset': 25,
                'page': 1,
                'output': 'json'
                }
        result = requests.get(self.init_url, params=payload)
        json_data = json.loads(result.text)
        try:
            max_count = int(json_data['count'])//25 + 1 #获取最大页码数量
        except Exception:
            return ''
        for one_page in range(1, max_count+1):
            payload['page'] = one_page
            result = requests.get(self.init_url, params=payload)
            time.sleep(0.1)
            json_data_page = json.loads(result.text)
            pois = json_data_page['pois']
            one_city_pois.extend(pois)
        return one_city_pois

    def get_city_lst(self):
        '''对文件读取，获取每个省、县级单位的名称和编码'''
        with open(self.city_lst, encoding='utf-8') as f:
            reader = [one.split(',') for one in f.read().split('\n')]
        return reader[1:]

    def main(self, keyw):
        piece_of_city = []
        num = 0
        for province, city, adcode in self.get_city_lst():
            print('{}省{}正在访问'.format(province, city))
            try:
                one_city_location = self.spiders(keyw, adcode)
                num = len(one_city_location) + num
                df_one_city_location = pd.DataFrame(one_city_location)
                piece_of_city.append(df_one_city_location)
            except Exception:
                pass
            print('一共有{}家, {}下载成功'.format(num, city))
            continue
        all_city_location = pd.concat(piece_of_city, ignore_index=True)
        all_city_location.to_excel('d:\\经纬度\\1102\\{}1102.xlsx'.format(keyw.replace('|', '_')))
        return 'all is ok, max_num is {}'.format(str(num))

    def all_brand(self):
        # brand_lst = [
        #         '太平鸟|peacebird', '以纯|yishion','江南布衣|JNBY', '伊芙丽|eifini',
        #         '海澜之家|hlamall', '美特斯邦威|metersbonwe', 'ONlY', '韩都衣舍|HSTYLE',
        #         '优衣库|uniqlo', '拉夏贝尔|lachapelle', 'me&city', '杰克琼斯|jackjones',
        #         '阔色|kuose', '速写|croquis|less', 'Lily', '播|broadcast', 'GXG',
        #         '欧时力|ochirly', '茵曼|inman', '若己|Aself', 'Material girl',
        #         'trendiano', 'lilbetter', 'viishow', 'jucy judy', 'H&M', 'Zara',
        #         '真维斯|jeanswest', '唐狮|tonlion', '爱居兔|Eichitoo', 'vero moda',
        #         '马克华菲|fairwhale', '佐丹奴|Giordano', '卡宾|cabbeen']
        brand_lst = ['唐狮|tonlion', '爱居兔|Eichitoo', 'vero moda', '马克华菲|fairwhale', '佐丹奴|Giordano', '卡宾|cabbeen']
        for one_brand in brand_lst:
            print(one_brand)
            print(self.main(one_brand))
            print('\n*****************************\n')
        else:
            return '所有的均已完成'


if __name__ == '__main__':
    amap = AmapCrwaler()
    # print(amap.get_city_lst())
#    amap.main()
    amap.all_brand()

