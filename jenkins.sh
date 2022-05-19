#!/bin/bash
#IP=`ifconfig eth0 | awk -F '[ :]+' 'NR==2 {print $3}'`
#cat=`cat /var/lib/jenkins/secrets/initialAdminPassword`
systemctl stop firewalld
systemctl disenable firewalld
sleep 2s
yum -y install lrzsz vim net-tools wget git htop
echo "lrzsz,vim,net-tools,wget,git,htop安装成功"
sleep 2s
echo "开始安装JDK!!!"
yum install -y java-1.8.0-openjdk-devel.x86_64
sleep 2s
java -version
if [ $? -eq 0 ];then
	echo "JDK安装完成!"
else
	echo "JDK安装失败,重新安装~" && yum install -y java-1.8.0-openjdk-devel.x86_64
fi

#由于下载网速比较慢,所有注释掉了
wget http://mirrors.jenkins-ci.org/redhat/jenkins-2.298-1.1.noarch.rpm && rpm -ivh jenkins-2.298-1.1.noarch.rpm
if [ $? -eq 0 ];then
	echo "Jenkins安装成功"
else
	echo "Jenkins安装失败,重新安装" && wget http://mirrors.jenkins-ci.org/redhat/jenkins-2.298-1.1.noarch.rpm && rpm -ivh jenkins-2.298-1.1.noarch.rpm
fi

#把jenkins-rpm手动上传到/opt下即可
#sleep 2s 
#cd /opt && rpm -ivh jenkins-2.298-1.1.noarch.rpm

sleep 2s

grep JENKINS_USER= /etc/sysconfig/jenkins | sed -i 's#JENKINS_USER="jenkins"#JENKINS_USER="root"#g' /etc/sysconfig/jenkins

sleep 2s 
systemctl start jenkins
systemctl status jenkins
if [ $? -eq 0 ];then
	echo "jenkins启动成功!请在浏览器输入本地IP:8080端口即可访问"
else
	echo "jenkins启动失败,请手动启动谢谢!"
fi
sleep 2s
netstat -tnulp |grep 8080
sleep 5s
if [ $? -eq 0 ];then
	echo "请手动打开/var/lib/jenkins/secrets/initialAdminPassword获取初始密码"
else
	echo "请手动打开/var/lib/jenkins/secrets/initialAdminPassword获取初始密码"
fi
sleep 3s
cat /var/lib/jenkins/secrets/initialAdminPassword