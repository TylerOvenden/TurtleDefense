classdef node 
    properties %not tunable properties 
        %ie cannot be changed during run time
       row;
       column;
       gamma%persistance
       beta;%strength
       state;
    end
     methods
         %Constructor
         function obj = node(row,column)
            obj.row = row;
            obj.column = column;
        end
         %Probability
         function p1 = SIIS(t,beta,gamma,row,column)
           for i = -1:1
               for j = -1:1
                   zeta1 = zeta *( 1 - p1(t-1,beta,gamma,row+i,column+j));
                   zeta2 = zeta *( 1 - p2(t-1,beta,gamma,row+i,column+j));     
               end
           end
           T1 = (1-zeta1)*zeta1;
           T2= (1-zeta2)*zeta2;
           t.state = (1-T1 - T2);
            
         end
    end
   % methods%constructor
    %    function obj = node(varargin)
     %      setProperties(obj,naragin,varargin{:});
     % end
    %end
    methods(Static)
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
       % function stepImpl(obj,t)
            %place holder code so it will compile to check for errors
           % if rand()*100*(t-1) <30 
            %    obj.state = 1;
            %end
        %end
    end
end

