function T = tau(z)
   zeta1 =z(1);
   zeta2 =z(2);
    
   T(1) = (1-zeta1)*zeta2;
   T(2) = (1-zeta2)*zeta1;
    
end