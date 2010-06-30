<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8" import="com.bupticet.util.RequestUtils"%>
<%
	//request.getRequestDispatcher( "/404").forward(request, response);
	//response.sendRedirect(request.getContextPath()+"/404");
%>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>错误的访问路径</title>
<link rel="icon" type="image/gif"
	href="<%=request.getContextPath()%>/s/icon/16.gif" />
<link
	href="<%=request.getContextPath()%>/s/themes/<%=RequestUtils.getSiteTheme(request)%>/css/error.css"
	rel="stylesheet" type="text/css"></link>
</head>
<body>
<div id="errorBody">
<div id="header">404错误</div>
<div id="content">您是不是输入了错误的访问路径？</div>
<div id="container">
<%
			if (request.getHeader("referer") != null
			&& !"".equals(request.getHeader("referer"))) {
%>
 <a href="<%=request.getHeader("referer")%>" title="点击此处后退">后退</a>
	<%
 }
 %> <a href="<%=request.getContextPath()%>/" title="点击此处返回首页">返回首页</a>
</div>
</div>
</body>
</html>