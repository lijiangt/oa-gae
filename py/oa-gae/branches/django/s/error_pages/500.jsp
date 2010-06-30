<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8" isErrorPage="true"
	import="com.bupticet.util.RequestUtils,
			com.bupticet.util.StringUtils,
			org.apache.commons.logging.LogFactory,
			com.opensymphony.xwork2.ognl.OgnlValueStack,
			org.apache.struts2.ServletActionContext"%>
<%
//request.getRequestDispatcher( "/404").forward(request, response);
//response.sendRedirect(request.getContextPath()+"/404");
Throwable e = exception;
OgnlValueStack stack = (OgnlValueStack)request.getAttribute(ServletActionContext.STRUTS_VALUESTACK_KEY);
if(stack!=null){
	e = (Throwable)stack.findValue("exception");
}
if(e!=null){
	LogFactory.getLog(this.getClass()).fatal(StringUtils.getTraceOfException(e));
}
%>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>服务器内部错误</title>
<link rel="icon" type="image/gif"
	href="<%=request.getContextPath()%>/s/icon/16.gif" />
<link
	href="<%=request.getContextPath()%>/s/themes/<%=RequestUtils.getSiteTheme(request)%>/css/error.css"
	rel="stylesheet" type="text/css"></link>
</head>
<body>
<div id="errorBody">
<div id="header">500错误</div>
<div id="content">您是不是执行了非法操作？错误信息：<br /><%=e!=null?e.getMessage():""%></div>
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