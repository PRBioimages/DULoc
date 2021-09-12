
clearvars; close all; clc 

%% ============== Read Image ======================= 

load('Murphy_new_dataset.mat') % Murphy dataset 
M_data = mix_prob_arr(:,:);
R_Lyso = f_Lyso(:);
R_Mito = f_Mito(:);
clear mix_prob_arr; 
[N,L] = size(M_data);
S = M_data';clc 

%% =============== Endmembers =====================

% [Ae, idx_vca, Rp] = vca(S,'Endmembers',4);
R = [R_Lyso, R_Mito];

P = size(R,2);

hFig = figure;
set(hFig, 'Position', [300 500 300 200])
plot(R); 
axis([1 L 0 0.5]);
legend('Lyso','Mito');
AxisFont
                             
%% =============== Test FCLS =====================

H = R'*R;
f = -R'*S;
l = zeros(P,1);
A = ones(1,P);
b = 1;
X_FCLS = zeros(P,N);

for i=1:N
    X_FCLS(:,i) = qpas(H,f(:,i),[],[],A,b,l);
end

RE_FCLS = ErrComput(S,R*X_FCLS);
Angle_FCLS = Compute_avg_angle(S,R*X_FCLS);

realrate = [realLysorate(:), realMitorate(:)];
FCLS_corrcoef = corrcoef(X_FCLS,realrate');
FCLS_MSE = sum(sum((X_FCLS-realrate').^2))/N;
disp(FCLS_MSE)

%% =============== Test ExtR =====================
               
RExt = zeros(L,P+(P^2-P)/2);
RExt(:,1:P) = R;
cnt = P+1;
for i= 1:P
    for j=i+1:P
        RExt(:,cnt) = R(:,i).*R(:,j);
        cnt = cnt+1;
    end
end

Pext = cnt-1;

[X_RExtR, t_RExtR] = FCLS(S,RExt);
F_RExtR = RExt(:,P+1:end)*X_RExtR(P+1:end,:);

RE_RExtR = ErrComput(S,R*X_RExtR(1:P,:)+F_RExtR);
Angle_RExtR = Compute_avg_angle(S,R*X_RExtR(1:P,:)+F_RExtR);

realrate = [realLysorate(:), realMitorate(:)];
R_RExtR_corrcoef = corrcoef(X_RExtR(1:P,:),realrate');
RExtR_MSE = sum(sum((X_RExtR(1:P,:)-realrate').^2))/N;
disp(RExtR_MSE)

%% =============== Test khype (G) =====================

lambda = 100;
mu = 0.01;

tmp = pdist2(R,R);
par = 1; % Gaussian
sigma = par*max(tmp(:)); 
% sigma = 1;
[X_khype, F_khype, K_Khype] = khype3(sigma,lambda,mu,N,S,R);

realrate = [realLysorate(:), realMitorate(:)];
R_khype_corrcoef = corrcoef(X_khype,realrate');
MSE_khype = sum(sum((X_khype-realrate').^2))/N;
disp(MSE_khype)
RE_khype = ErrComput(S,R*X_khype+F_khype);
Angle_khype = Compute_avg_angle(S,R*X_khype+F_khype);

%% =============== NDU (P) =====================
% lambda = 10;
% mu = 0.0001;
sub_N = 100;
whole_X = zeros(P,N); 
whole_F = zeros(L,N);

for i=1:floor(N/sub_N)
    ni = (i-1)*sub_N+1:i*sub_N;
    Si = S(:,ni);
    
    V = cell(1,sub_N);
    for ii=1:sub_N
        V{1,ii} = [Si(:,ii) Si(:,ii)];
    end

    [X_FCLS, t_FCLS] = FCLS(Si,R);
    disp(size(X_FCLS))
    disp(size(t_FCLS))
    % abd_map2_i = reshape(X_FCLS,N,P)';
    % abd_map2_i = reshape(abd_map2_i,N,P)';

    str = 'Separable'; % 'full'; %'Separable'or'Transformable'
    par = 0; % 0: Polynomial kernel & 1: Gaussian kernel
 
    [Xi, Fi, t_NDU, K_NDU] = NDU(Si,R,V,lambda,mu,par,str);
    whole_X(:,ni)=Xi;
    whole_F(:,ni)=Fi;
end

RE_NDU = ErrComput(S,R*whole_X+whole_F);
Angle_NDU = Compute_avg_angle(S,R*whole_X+whole_F);

realrate = [realLysorate(:), realMitorate(:)];
R_corrcoef = corrcoef(whole_X,realrate');
MSE = sum(sum((whole_X-realrate').^2))/N;
disp(MSE)


% V = cell(1,N);
% for ii=1:N
%     V{1,ii} = [S(:,ii) S(:,ii)];
% end
% 
% [X_FCLS, t_FCLS] = FCLS(S,R);
% disp(size(X_FCLS))
% disp(size(t_FCLS))
% % abd_map2_i = reshape(X_FCLS,N,P)';
% % abd_map2_i = reshape(abd_map2_i,N,P)';
% 
% str = 'Transformable'; % 'full'; %
% par = 0; % Polynomial
% [X, F, t_NDU, K_NDU] = NDU(S,R,V,lambda,mu,par,str);
% disp(size(X))
% disp(size(F))
% % X = X';   % coefficient
% % F = F';
% RE_NDU = ErrComput(S,R*X+F);
% Angle_NDU = Compute_avg_angle(S,R*X+F);
% 
% realrate = [realLysorate(:), realMitorate(:)];
% R_corrcoef = corrcoef(X,realrate');
% MSE = sum(sum((X-realrate').^2))/N;
% disp(MSE)



