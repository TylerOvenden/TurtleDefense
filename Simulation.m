t = linspace(0,10);
N = 100;
temp= zeros(N,N);
%Create Array of nodes
network1 = ObjectArray(N);
network2 = ObjectArray(N);
%First network occupies the first N nodes
for k = 1:N
    for j = 1:N
    network1(k,j) = node(k,j);
    end
end
%Second network occupies the second N nodes
for k = 1:N
    for j = 1:N
        network2(k,j) = node(k,j);
    end
end
%create adjaceny matrixes of both networks
A1 = randi([0,1],[N,N]);
A2 = randi([0,1],[N,N]);

for i = 0:N
    for j =0:N
    network1[i].state = network1(i).SIIS()
    end
end
