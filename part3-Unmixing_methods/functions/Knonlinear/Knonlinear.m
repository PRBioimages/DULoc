function [a_est, b_est, KM] = Knonlinear(par,ksi,mu,N,r,M)

% ============  Parameters to tune ======================== 
% Gaussian kernel bandwidth : 
% par = 2;
% Regualrization parameter : 
% \mu in the paper = 1/C
% C = 100;
% C = 1/mu;
%  ============== Image generation  =======================
[L, R] = size(M);

% ============= nonlinear kernel calculation =================
if par==0
    KM = (M*M').^2; 
    KM = KM/max(KM(:)); 
else
    Q=eye(R)/par^2;
    MQM=M*Q*M';
    dMQM = diag(MQM);
    KM = exp(-0.5*(dMQM*ones(L,1)'+ones(L,1)*dMQM'-2*M*Q*M'));
end
% For using the polynomial proposed polynomial kernel, remove the
% comment symbol:
% KM = (1+1/R^2*(M-0.5)*(M-0.5)').^2;

M1 = M*ones(R,1);
a_est = zeros(R,N);
b_est = zeros(L,N);
MM = M*M';

% =================== Algorithm K-Hype =======================
for n = 1 : N
    y = r(:,n);
   % max dual
    K = (1/ksi)*KM+(1/mu)*MM; % 1*MM+KM;
    K = K+eye(L);
    H = [K,    (1/mu)*M,    -(1/mu)*M1;
         (1/mu)*M',  (1/mu)*eye(R), -(1/mu)*ones(R,1);     
         -(1/mu)*M1', -(1/mu)*ones(R,1)',(1/mu)*R];
    H=(H+H')/2;
    H=H+0.0000*eye(L+R+1);
 
    f = -[y;zeros(R,1);-1];
    A = -[zeros(R,L),eye(R),zeros(R,1)];
    b = zeros(R,1);
    
    z = qpas(H,f,A,b); % ,Aeq,beq);
    beta=z(1:L);
    gam=z(L+1:L+R);
    lambda=z(end);
    h = (M'*beta+gam-lambda)/mu;
    a_est(:,n)=h;
    b_est(:,n)=KM*beta/ksi;
end



