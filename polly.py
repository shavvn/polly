from abc import abstractmethod


class Polly(object):
    """
    A base class specify interfaces and do basic stuff such as init/set params
    """
    def __init__(self, *args, **kwargs):
        """
        set default params and user defined ones
        :return: self.params
        """
        # have a list of default params, change them if necessary
        self.params = {
            "title": "Default Title",
            "width": 0.4,
            "data": None,
        }
        self.plot_type = "Default"
        self.set_params(args, kwargs)

    def get_params(self):
        return self.params

    def set_params(self, *args, **kwargs):
        if len(args) == 1:  # pass a file or data structure
            if ".csv" in args:  # a csv file
                self.parse_csv(args)
            else:
                if isinstance(args, dict):  # a dict instance
                    for key, value in args.items():
                        if key in self.params:
                            self.params[key] = value
        elif len(args) == 0:
            pass
        else:
            print ("shouldn't have more than 1 args")
            exit(1)
        # process kwargs
        for key, value in kwargs.items():
            if key in self.params:
                self.params[key] = value

    def add_params(self, **kwargs):
        """
        add new parameters from a dict structure
        :param kwargs: key and value pairs
        :return: nothing... params should be updated
        """
        for key, value in kwargs.items():
            self.params[key] = value

    @abstractmethod
    def plot(self):
        """
        Abstract method, Subclass must implement this
        :return: None
        """
        raise NotImplementedError("Subclass must implement abstract method")
    
    @abstractmethod
    def parse_csv(self, file_name):
        """
        :param file_name: the csv name to be parsed
        :return: params that could be used to plot
        """
        raise NotImplementedError("Subclass must implement abstract method")
