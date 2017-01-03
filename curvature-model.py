import os
import errno
import numpy as np
import matplotlib.pyplot as plt

tickers = ['AAPL','AXP','BA','CAT','CSCO','CVX','DD','DIS','GE','GS','HD','IBM','INTC','JNJ','JPM','KO','MCD','MMM','MRK','MSFT','NKE','PFE','PG','TRV','UNH','UTX','V','VZ','WMT','XOM']

def read_file(filename):
    '''
    Read data from the specified file.  Split the lines and convert
    float strings into floats.  Assumes the first row contains labels
    for the columns.

    Inputs:
      filename: name of the file to be read as string

    Returns:
      (list of strings, 2D array)
    Courtesy of Borja for use in CS 121
    '''
    with open(filename) as f:
        labels = f.readline().strip().split(',')
        data = np.loadtxt(f, delimiter=',', dtype=np.float64)
        return labels, data

def create_folder(foldername):
    '''
    Creates folder if folder does not exist
    '''
    try:
        os.makedirs(foldername)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def get_data(filename):

    '''
    Given a csv file of data as a string, separate out time,
    dependent variables, and price

    First row of CSV file must be variable labels
    First column must be time (or other independent variable)
    Remaining columns are independent variables (volume, price change, etc.)
    Rightmost column is price.

    returns: tuple: (time, dependent vars, price, dependent labels)
    '''

    data = read_file(filename)

    time = data[1][:,0] #indep var
    dep_vars = data[1][:,1:-1]
    price = data[1][:,-1]
    dep_var_labels = data[0][1:-1]

    return (time,dep_vars,price,dep_var_labels)

def discrete_curvature(dataset):
    '''
    Takes in a 2D numpy array where first
    column is time, rest are variables
    '''
    points = dataset[:,1:]
    t = dataset[:,0]

    num_points = points.shape[0]

    k = np.empty(points.shape[0])

    for i in range(num_points - 2):
        df_1 = points[i + 1,:] - points[i,:]
        ds_1 = np.sqrt(sum(df_1 ** 2))
        df_2 = points[i + 2,:] - points[i + 1,:]
        ds_2 = np.sqrt(sum(df_2 ** 2))
        d2f = df_2/ds_2 - df_1/ds_1 	# Difference between unit tangent vectors
        ds2 = (ds_2 + ds_1)/2				# Approximate arclength

        curvature = np.sqrt(sum(d2f ** 2))/ds2

        k[i + 1] = curvature

        rv = np.empty((num_points,2))

    for j in range(num_points):
        rv[j][0] = t[j]
        rv[j][1] = k[j]

    return rv


def discrete_curvature_by_var(filename, variables, plot=False, outputfilename=None):
    '''
    So you have a csv file as dictated in get_data.
    You pick the variables you want in your curvature model
    as a list of strings.
    Returns a three column array, first column is time,
    second is curvature, third is price
    Plot is a boolean. Set to True if you want a plot, False elsewise. Plots curvature against price
    Outputfilename is a string, set it to the name of the file
    you want the results to be saved as. Will be a csv (no need to add
    file extension). If set to None, file will not save.
    '''
    data = get_data(filename)
    time = data[0]
    dep_vars = data[1]
    prices = data[2]
    dep_var_labels = data[3]

    vars_to_be_tested = []
    num_points = dep_vars.shape[0]

    for variable in variables:
        assert variable in dep_var_labels, "Variable is not valid: %r" %variable #makes sure I'm testing valid variables
        vars_to_be_tested.append(dep_var_labels.index(variable))

    dataset = np.empty((num_points,len(vars_to_be_tested) + 1))

    for i in range(num_points):
        dataset[i][0] = time[i]
        for j in range(len(vars_to_be_tested)):
            dataset[i][j + 1] = dep_vars[i][vars_to_be_tested[j]]

    time_vs_curvature = discrete_curvature(dataset)
    time_vs_curvature_vs_price = np.column_stack((time_vs_curvature,prices))

    if plot:
        plt.plot(time_vs_curvature_vs_price[:,0],time_vs_curvature_vs_price[:,1])
        plt.plot(time_vs_curvature_vs_price[:,0],time_vs_curvature_vs_price[:,2])
        #plt.show()
        create_folder("figures")
        plt.savefig(os.path.join("figures", outputfilename + ".pdf"))
    if outputfilename != None:
        assert type(outputfilename) == str, "Filename must be str!"
        create_folder("data")
        np.savetxt(os.path.join("data", outputfilename + ".csv"), time_vs_curvature_vs_price, delimiter = ",")

    #return time_vs_curvature_vs_price

def main():
    cdir = os.getcwd()
    #os.chdir(os.path.join(cdir,"IndividualStockCSVs"))
    for ticker in tickers:
        discrete_curvature_by_var(os.path.join(cdir,"IndividualStockCSVs",ticker+".csv"), ["VolumePercentChange","IntradayPercentPriceChange"], plot=True, outputfilename=ticker)
        plt.clf()

if __name__ == '__main__':
    main()
