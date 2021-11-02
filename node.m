classdef node < matlab.system
    properties(private) %not tunable properties 
        %ie cannot be changed during run time
       persistance;
       strength;
    end
    properties(DiscreteState) %I think we put the states here
        suscetiple; %if not we can use to label states by 0,1,2
    end
    methods%constructor
        function obj = node(varargin)
           setProperties(obj,naragin,varargin{:});
        end
    end
    methods (Static)
        function attack()        
        end
    end
    methods(Access=protected)
    end
end

