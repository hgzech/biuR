# biuR
> An extract of the BIU R functionality, without any dependency on <a href='https://github.com/thiesgehrmann/biuR'>biu</a>.


## Install

`pip install biur`

## How to use

```python
import biur.wrapper
import matplotlib.pylab as plt
import pandas as pd
```

```python
R = biur.wrapper.R()
```

## Push some data

```python
R.push(n=5000, mean=10, var=6, question="How many apples do you eat per day?")
```

## Run some commands

```python
R("""
    dist <- rnorm(n, mean, var)
    print(mean(dist))
""", get=False)
```

    [1] 10.04324


## Get some data

```python
dist = R.get("dist")
dist_alt = R("dist", get=True) # the get parameter is True by default
_ = plt.hist(dist, bins=50)
```


![png](docs/images/output_10_0.png)


## Do it all at the same time

```python
dist = R("""rnorm(n, mean, var)""",
         push=dict(n=5000, mean=10, var=6, question="How many apples do you eat per day?"))
_ = plt.hist(dist, bins=50)
```


![png](docs/images/output_12_0.png)


## Dataframes also work as expected

```python
df  = pd.DataFrame(dist.reshape(500,10), columns=["C%d" % (i+1) for i in range(10)])
df2 = R("""df*2""", push=dict(df=df))
df2.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>C1</th>
      <th>C2</th>
      <th>C3</th>
      <th>C4</th>
      <th>C5</th>
      <th>C6</th>
      <th>C7</th>
      <th>C8</th>
      <th>C9</th>
      <th>C10</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>500.000000</td>
      <td>500.000000</td>
      <td>500.000000</td>
      <td>500.000000</td>
      <td>500.000000</td>
      <td>500.000000</td>
      <td>500.000000</td>
      <td>500.000000</td>
      <td>500.000000</td>
      <td>500.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>19.664014</td>
      <td>19.844730</td>
      <td>21.397676</td>
      <td>20.316715</td>
      <td>19.915327</td>
      <td>20.479617</td>
      <td>20.606811</td>
      <td>20.671680</td>
      <td>19.978792</td>
      <td>20.363389</td>
    </tr>
    <tr>
      <th>std</th>
      <td>12.082482</td>
      <td>11.829318</td>
      <td>11.756079</td>
      <td>12.228085</td>
      <td>11.878440</td>
      <td>12.626452</td>
      <td>11.560421</td>
      <td>12.360558</td>
      <td>12.425381</td>
      <td>12.545196</td>
    </tr>
    <tr>
      <th>min</th>
      <td>-28.185781</td>
      <td>-11.851668</td>
      <td>-14.899577</td>
      <td>-15.940758</td>
      <td>-23.651277</td>
      <td>-17.811376</td>
      <td>-13.721199</td>
      <td>-17.615716</td>
      <td>-18.421257</td>
      <td>-22.172515</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>11.909300</td>
      <td>12.042162</td>
      <td>13.257103</td>
      <td>12.162031</td>
      <td>12.214617</td>
      <td>11.778717</td>
      <td>12.920449</td>
      <td>12.178726</td>
      <td>11.741882</td>
      <td>12.254866</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>19.316743</td>
      <td>19.564965</td>
      <td>20.988669</td>
      <td>20.498992</td>
      <td>19.765990</td>
      <td>20.166144</td>
      <td>20.278277</td>
      <td>20.020587</td>
      <td>20.054040</td>
      <td>20.275403</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>27.771991</td>
      <td>28.085157</td>
      <td>29.174137</td>
      <td>28.447980</td>
      <td>28.061103</td>
      <td>28.312460</td>
      <td>28.384447</td>
      <td>28.869581</td>
      <td>28.670938</td>
      <td>29.319559</td>
    </tr>
    <tr>
      <th>max</th>
      <td>53.658666</td>
      <td>59.740534</td>
      <td>58.531887</td>
      <td>57.402270</td>
      <td>55.351012</td>
      <td>52.867132</td>
      <td>56.286094</td>
      <td>55.596513</td>
      <td>50.953409</td>
      <td>58.989365</td>
    </tr>
  </tbody>
</table>
</div>



## Some additional stuff

### Dates

```python
from datetime import datetime
R("""print(today)""", push=dict(today=datetime.today()), get=False)
```

    [1] "2021-11-15 14:59:14 EET"


### Dictionaries

> Note that individual numbers do not exist in R (everything is a vector) so it is impossible to transform this back perfectly.

```python
R.push(mydict={"A":10, "B":20, "C":40})
R("""
    mydict$D <- 60
    mydict""")
```




    {'A': [10], 'B': [20], 'C': [40], 'D': [60.0]}


