package com.yahooface.android;

import java.io.IOException;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ByteArrayEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.params.CoreConnectionPNames;
import org.apache.http.util.EntityUtils;

import android.app.Activity;
import android.util.Log;

/**
 * @author LDM 
 * @fileName BaseHttpPost.java
 * @date 2012-9-24 上午9:19:35
 * 客户端HTTP POST请求工具类
 */
public class BaseHttpPost {

	public static String url = "";//接口地址

	/**
	 * 
	 * @param serviceName接口名称(预留的，没用可以删除)
	 * @param bytes 向服务器写入byte[]格式数据(可以将图片及录像转成成byte[])
	 * @return 上传成功失败的返回标识(根据需求，如没有返回可以删除)
	 */
	public synchronized static String Comm(String serviceName, byte[] bytes) {
		String result = null;
		try {
			/************* 创建HttpClient及HttpPost对象 **************/
			HttpClient httpClient = getHttpClient();
			HttpPost httpPost = getHttpPost();
			
			/************* 向服务器写入数据 **************/
			write(httpPost, bytes);
			
			/************* 开始执行命令 ******************/
			HttpResponse httpResponse = httpClient.execute(httpPost);
			
			/***************接收客户端返回请求状态**************/
			int code = httpResponse.getStatusLine().getStatusCode();
			if (code == 200) {//200请求成功
				HttpEntity he = httpResponse.getEntity();
				//得到的返回数据，具体会返回什么内容找你们写服务端的，如果没有返回可以删除
				result = EntityUtils.toString(he);
			} else {//请求失败，code为异常编码
				Log.e("lidm", "网络请求错误码 ：" + code);
			}
		} catch (ClientProtocolException e) {
			e.printStackTrace();
			Log.e("lidm", "ClientProtocolException");
		} catch (IOException e) {
			e.printStackTrace();
			Log.e("lidm", "IOException");
		} catch (Exception e) {
			e.printStackTrace();
			Log.e("lidm", "Exception");
		}
		return result;
	}

	/**
	 * 使用ByteArrayEntity向服务器写入数据
	 * @param httpPost
	 * @param bytes
	 */
	private static void write(HttpPost httpPost, byte[] bytes) {
		httpPost.setEntity(new ByteArrayEntity(bytes));
	}

	/**
	 * 暂时设置的text/xml，如果不好用可以自行修改（网上很多自己找）
	 * @return
	 */
	private static HttpPost getHttpPost() {
		HttpPost httpPost = new HttpPost(url);
		httpPost.setHeader("Content-Type", "text/xml");
		return httpPost;
	}


	/**
	 * 创建HttpClient对象设置超读取超时及等待超时时间60秒
	 * @return
	 */
	private static HttpClient getHttpClient() {
		HttpClient httpClient = new DefaultHttpClient();
		httpClient.getParams().setParameter(CoreConnectionPNames.CONNECTION_TIMEOUT, 60*1000); 
		httpClient.getParams().setParameter(CoreConnectionPNames.SO_TIMEOUT, 60*1000);
		return httpClient;
	}
}