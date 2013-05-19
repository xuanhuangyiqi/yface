package com.yahooface.android;

import java.util.Locale;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ImageButton;
import android.widget.Toast;

import com.gmail.yuyang226.flickrj.sample.android.tasks.GetOAuthTokenTask;
import com.gmail.yuyang226.flickrj.sample.android.tasks.LoadUserTask;
import com.gmail.yuyang226.flickrj.sample.android.tasks.OAuthTask;
import com.googlecode.flickrjandroid.oauth.OAuth;
import com.googlecode.flickrjandroid.oauth.OAuthToken;
import com.googlecode.flickrjandroid.people.User;
import com.yahooface.http.HttpTask;

public class YahooCameraActivity extends UpdateActivity {
	
	public static final String CALLBACK_SCHEME = "yahooface-oauth"; //$NON-NLS-1$
	public static final String PREFS_NAME = "flickrj-android-sample-pref"; //$NON-NLS-1$
	public static final String KEY_OAUTH_TOKEN = "flickrj-android-oauthToken"; //$NON-NLS-1$
	public static final String KEY_TOKEN_SECRET = "flickrj-android-tokenSecret"; //$NON-NLS-1$
	public static final String KEY_USER_NAME = "flickrj-android-userName"; //$NON-NLS-1$
	public static final String KEY_USER_ID = "flickrj-android-userId"; //$NON-NLS-1$
	public static final String KEY_TRAINED_ID = "flickrj-android-trained"; //$NON-NLS-1$
	public static boolean isNewToken = false;

	private ImageButton loginbtn;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_yahoo_camera);
        loginbtn = (ImageButton)findViewById(R.id.loginbtn);
        loginbtn.setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				OAuth oauth = getOAuthToken();
//				if (oauth == null || oauth.getUser() == null) {//之前未登陆过
//					isNewToken = true;
//					OAuthTask task = new OAuthTask(YahooCameraActivity.this);//加载页面执行登陆、授权
//					task.execute();
//				} else {
//					load(oauth);//从手机缓存的信息中获取用户上次登陆的信息
//				}
				
				Intent intent = new Intent(YahooCameraActivity.this, CameraActivity.class);
				startActivity(intent);
				
			}
		});
    }
    
    /* (non-Javadoc)
	 * @see android.app.Activity#onNewIntent(android.content.Intent)
	 */
	@Override
	protected void onNewIntent(Intent intent) {
		//this is very important, otherwise you would get a null Scheme in the onResume later on.
		setIntent(intent);
	}
	
	//获取到的用户信息,记录到全局变量
	public void setUser(User user) {
		
		Account.setUser(user.getUsername());
		Account.setUserId(user.getId());
		Log.v("isNewToken",String.valueOf(isNewToken));
		if(isNewToken)
			connect();
		update();
	}
    private void connect() { 
    	Log.v("connect called","connect called");
        HttpTask task = new HttpTask(this,this,""); 
        String url = this.getResources().getString(R.string.serverip)+this.getResources().getString(R.string.loginposturl)+"?token="+Account.getOauthToken()+"&secret="+Account.getTokenSecret()+"&username="+Account.getUser()+"&flickr_id="+Account.getUserId();
        System.out.println("login post url: "+url);
        task.execute("POST",url);   
    } 
    
	@Override
	public void update() {
		// TODO Auto-generated method stub
		//Toast.makeText(context, text, duration)
		if(!Account.trained)
		{
			Intent intent = new Intent(YahooCameraActivity.this, PersonInfoActivity.class);
			startActivity(intent);
		}
		else
		{
			Intent intent = new Intent(YahooCameraActivity.this, CameraActivity.class);
			startActivity(intent);
		}
	}

	private void load(OAuth oauth) {
		if (oauth != null) {
			new LoadUserTask(this, null).execute(oauth);
			//new LoadPhotostreamTask(this, listView).execute(oauth);
		}
	}
	//利用request token 获取access token
	@Override
	public void onResume() {
		super.onResume();
		Intent intent = getIntent();
		String scheme = intent.getScheme();
		OAuth savedToken = getOAuthToken();
		if (CALLBACK_SCHEME.equals(scheme) && (savedToken == null || savedToken.getUser() == null)) {
			Uri uri = intent.getData();
			String query = uri.getQuery();
			//logger.debug("Returned Query: {}", query); //$NON-NLS-1$
			String[] data = query.split("&"); //$NON-NLS-1$
			if (data != null && data.length == 2) {
				String oauthToken = data[0].substring(data[0].indexOf("=") + 1); //$NON-NLS-1$
				String oauthVerifier = data[1]
						.substring(data[1].indexOf("=") + 1); //$NON-NLS-1$
				//logger.debug("OAuth Token: {}; OAuth Verifier: {}", oauthToken, oauthVerifier); //$NON-NLS-1$

				OAuth oauth = getOAuthToken();
				if (oauth != null && oauth.getToken() != null && oauth.getToken().getOauthTokenSecret() != null) {
					GetOAuthTokenTask task = new GetOAuthTokenTask(this);
					task.execute(oauthToken, oauth.getToken().getOauthTokenSecret(), oauthVerifier);
				}
			}
		}

	}
    public void onOAuthDone(OAuth result) {
		if (result == null) {
			Toast.makeText(this,
					"Authorization failed", //$NON-NLS-1$
					Toast.LENGTH_LONG).show();
		} else {
			User user = result.getUser();
			OAuthToken token = result.getToken();
			if (user == null || user.getId() == null || token == null
					|| token.getOauthToken() == null
					|| token.getOauthTokenSecret() == null) {
				Toast.makeText(this,
						"Authorization failed", //$NON-NLS-1$
						Toast.LENGTH_LONG).show();
				return;
			}
			String message = String.format(Locale.US, "Authorization Succeed: user=%s, userId=%s, oauthToken=%s, tokenSecret=%s", //$NON-NLS-1$
					user.getUsername(), user.getId(), token.getOauthToken(), token.getOauthTokenSecret());
			Toast.makeText(this,
					message,
					Toast.LENGTH_LONG).show();
			Account.setOauthToken(token.getOauthToken());
			Account.setTokenSecret(token.getOauthTokenSecret());
			saveOAuthToken(user.getUsername(), user.getId(), token.getOauthToken(), token.getOauthTokenSecret());
			load(result);
		}
	}
    
    
    public OAuth getOAuthToken() {
    	 //Restore preferences
        SharedPreferences settings = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
        String oauthTokenString = settings.getString(KEY_OAUTH_TOKEN, null);
        String tokenSecret = settings.getString(KEY_TOKEN_SECRET, null);
        Account.setTrained(settings.getBoolean(KEY_TRAINED_ID,false));
        
        if (oauthTokenString == null && tokenSecret == null) {
        	//logger.warn("No oauth token retrieved"); //$NON-NLS-1$
        	return null; 	
        }
        OAuth oauth = new OAuth();
        String userName = settings.getString(KEY_USER_NAME, null);
        String userId = settings.getString(KEY_USER_ID, null);
        if (userId != null) {
        	User user = new User();
        	user.setUsername(userName);
        	user.setId(userId);
        	oauth.setUser(user);
        }
        
		Account.setOauthToken(oauthTokenString);
		Account.setTokenSecret(tokenSecret);
		Account.setUser(userName);
		Account.setUserId(userId);
		
		//System.out.println("token："+oauthTokenString);
		//System.out.println("token secret："+tokenSecret);
		
		
        OAuthToken oauthToken = new OAuthToken();
        oauth.setToken(oauthToken);
        oauthToken.setOauthToken(oauthTokenString);
        oauthToken.setOauthTokenSecret(tokenSecret);
        
        //logger.debug("Retrieved token from preference store: oauth token={}, and token secret={}", oauthTokenString, tokenSecret); //$NON-NLS-1$
        return oauth;
    }
    
    public void saveOAuthToken(String userName, String userId, String token, String tokenSecret) {
    	//logger.debug("Saving userName=%s, userId=%s, oauth token={}, and token secret={}", new String[]{userName, userId, token, tokenSecret}); //$NON-NLS-1$
    	SharedPreferences sp = getSharedPreferences(PREFS_NAME,
				Context.MODE_PRIVATE);
		Editor editor = sp.edit();
		editor.putString(KEY_OAUTH_TOKEN, token);
		editor.putString(KEY_TOKEN_SECRET, tokenSecret);
		editor.putString(KEY_USER_NAME, userName);
		editor.putString(KEY_USER_ID, userId);
		editor.commit();
    }
}
