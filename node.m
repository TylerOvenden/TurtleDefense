classdef node 
    properties %not tunable properties 
        %ie cannot be changed during run time
       nodeNum;
       persistance;
       strength;
       state;
    end
     methods%Constructor
        function obj = node(nodeNum)
            obj.nodeNum=nodeNum;
        end
    end
   % methods%constructor
    %    function obj = node(varargin)
     %      setProperties(obj,naragin,varargin{:});
     % end
    %end
    methods (Static)
        function attack()        
        end
    end
   
    methods(Access=protected)
        function setupImpl (obj,in)
            obj.state = in;
        end
        function resetImpl(obj)
            obj.state = 0;
        end
        function stepImpl(obj,t)
            %%place holder code so it will compile to check for errors
            if rand()*100*(t-1) <30 
                obj.state = 1;
            end
        end
    end
end

