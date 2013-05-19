package com.yahooface.android;

import java.util.ArrayList;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.ProgressDialog;
import android.os.Bundle;
import android.os.Handler;
import android.widget.TextView;

import com.yahooface.http.HttpTask;

public class PersonActivity extends UpdateActivity{

	private ProgressDialog progressDialog = null;
    private Handler handler = new Handler();
    private TextView tv1,tv2,tv3,tv4,tv5,tv6;
    private TextView yahooname;
    
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		// TODO Auto-generated method stub
		super.onCreate(savedInstanceState);
		setContentView(R.layout.personalcenter);
		
		tv1 = (TextView)findViewById(R.id.yntitle1);
		tv2 = (TextView)findViewById(R.id.yncontent1);
		tv3 = (TextView)findViewById(R.id.yntitle2);
		tv4 = (TextView)findViewById(R.id.yncontent2);
		tv5 = (TextView)findViewById(R.id.yntitle3);
		tv6 = (TextView)findViewById(R.id.yncontent3);
		yahooname = (TextView)findViewById(R.id.yahooname);
		
		yahooname.setText(Account.getUser());
		
		String url = PersonActivity.this.getResources().getString(R.string.serverip)+ PersonActivity.this.getResources().getString(R.string.news)+"?username=obama";
		HttpTask task = new HttpTask(PersonActivity.this,PersonActivity.this,"please wait,loading news...");
		System.out.println(url);
		task.execute("GET",url);
	}
	void retrieve(String str)
	{
		Account.list = new ArrayList<Person>();
		try {
			JSONArray myJsonArray = new JSONArray(str);
			for(int i=0 ; i < myJsonArray.length() ;i++)
			   {
				    //获取每一个JsonObject对象
				    JSONObject myjObject = myJsonArray.getJSONObject(i);
				    if(i==0)
				    {
				    	tv1.setText(myjObject.getString("title"));
					    tv2.setText(myjObject.getString("abstract"));
				    }
				    if(i==1)
				    {
				    	tv3.setText(myjObject.getString("title"));
					    tv4.setText(myjObject.getString("abstract"));
				    }
				    if(i==2)
				    {
				    	tv5.setText(myjObject.getString("title"));
					    tv6.setText(myjObject.getString("abstract"));
				    }
				    
			   }

		} catch (JSONException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		//str = str.replace("[", "");
		//str = str.replace("]", "");
		//String[] persons = str.split("},{");
	}
	@Override
	public void update() {
		// TODO Auto-generated method stub
		System.out.println(Account.newsStr);
		retrieve(Account.newsStr);
	}
	 
}
