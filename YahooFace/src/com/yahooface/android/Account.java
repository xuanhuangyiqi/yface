package com.yahooface.android;

import java.util.ArrayList;

import org.json.JSONException;
import org.json.JSONObject;

public class Account {
	public static String user = null;
	public static String userId = null;
	public static String oauthToken = null;
	public static String tokenSecret = null;
	public static boolean trained = false;
	public static JSONObject jsonobj;
	public static String[] urls;
	public static ArrayList<Person> list = null;
	public static Person curPerson = null;
	public static String newsStr = "";
	
	public static String getUser() {
		return user;
	}
	public static boolean isTrained() {
		return trained;
	}
	public static void setTrained(boolean trained) {
		Account.trained = trained;
	}
	public static void setUser(String user) {
		Account.user = user;
	}
	public static String getUserId() {
		return userId;
	}
	public static void setUserId(String userId) {
		Account.userId = userId;
	}
	public static String getOauthToken() {
		return oauthToken;
	}
	public static void setOauthToken(String oauthToken) {
		Account.oauthToken = oauthToken;
	}
	public static String getTokenSecret() {
		return tokenSecret;
	}
	public static void setTokenSecret(String tokenSecret) {
		Account.tokenSecret = tokenSecret;
	}
	public static void buildJsonobj(String str)
	{
		try {
			jsonobj = new JSONObject(str);
			urls = jsonobj.getString("images").replace("[", "").replace("]", "").replace("\"", "").replace("\\", "").split(",");
			System.out.println("urls[0]" + urls[0]);
			//String id = obj.getString("id");
			//String version = obj.getString("version");
		} catch (JSONException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	
}
