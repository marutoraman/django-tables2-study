from django.shortcuts import render
from django.views import generic
from datetime import datetime
from django.contrib import messages
from django_tables2 import SingleTableView, RequestConfig
from ..models.torihiki import *
from ..tables.torihiki import * 
from setting.models.asin_group import *
from django.contrib.auth import get_user_model
User = get_user_model()



class TorihikiView(SingleTableView):
    table_class = TorihikiTable
    template_name = "torihiki/list.html"

    def get(self, request, *args, **kwargs):
        self.view_table(yahoo_account_id=None)
        # ヤフオクIDを取得
        yahoo_account_obj = User.objects.filter(account_id=self.request.user).first()
        context = {'table':self.torihiki_data_table1,'table2':self.torihiki_data_table2,'table3':self.torihiki_data_table3,
                   'table4':self.torihiki_data_table4,'table5':self.torihiki_data_table5,
                   'record_count':self.record_count1,'record_count2':self.record_count2,'record_count3':self.record_count3,
                   'record_count4':self.record_count4,'record_count5':self.record_count5,'torihiki_stat':TORIHIKI_STAT.CHOICE,
                   'selected_yahoo_account_id':yahoo_account_obj.yahoo_account_id.first(),
                   'yahoo_account_id_list': yahoo_account_obj.yahoo_account_id.all(),}
        
        return render(request, self.template_name,context=context)


    def post(self, request, *args, **kwargs):
        
        yahoo_account_id=request.POST.get("yahoo_account_id")
        
        # 発送完了ボタン押下時
        if "send-btn" in request.POST:
            checkbox_selection=request.POST.getlist("checkbox")
            torihiki_obj=TorihikiModel.objects.filter(id__in=checkbox_selection)
            for data in torihiki_obj:
                data.shipping_notice_stat = STAT.RESERVED #発送通知 > 予約済
                data.save()
                
        # 落札者評価ボタン押下時
        elif "hyouka-btn" in request.POST:
            checkbox_selection=request.POST.getlist("checkbox")
            torihiki_obj=TorihikiModel.objects.filter(id__in=checkbox_selection).all()
            for data in torihiki_obj:
                data.hyouka_flg=True #発送通知フラグを立てる
                data.save()
                
        # 評価文言設定の保存ボタン押下時
        elif "commit-data" in request.POST:
            hyouka_message=request.POST.get("hyouka_message")
            yahoo_account_id=request.POST.get("modale_yahoo_account_id")
            #HyoukaSetting.objects.filter(account_id=self.request.user,yahoo_account_id=yahoo_account_id).delete()
            #hyouka_setting_obj=HyoukaSetting(account_id=self.request.user,yahoo_account_id=yahoo_account_id,hyouka_message=hyouka_message)
            #hyouka_setting_obj.save()
            
        #hyouka_setting_obj=HyoukaSetting.objects.filter(account_id=self.request.user,yahoo_account_id=yahoo_account_id).first()
        #form=HyoukaSettingForm(instance=hyouka_setting_obj)
        self.view_table(yahoo_account_id)
        yahoo_account_obj = User.objects.filter(account_id=self.request.user).first()
        return render(request, self.template_name, {'table':self.torihiki_data_table1,'table2':self.torihiki_data_table2,'table3':self.torihiki_data_table3,'table4':self.torihiki_data_table4,'table5':self.torihiki_data_table5,
                                                'record_count':self.record_count1,'record_count2':self.record_count2,'record_count3':self.record_count3,'record_count4':self.record_count4,'record_count5':self.record_count5,
                                                'torihiki_stat':TORIHIKI_STAT.CHOICE,'form':'','yahoo_account_id_list': yahoo_account_obj.yahoo_account_id.all(),'selected_yahoo_account_id': yahoo_account_id}) 
        
    
    def view_table(self, yahoo_account_id):
        # 利益更新
        TorihikiModel().update_profit(self.request.user, yahoo_account_id)
        # TODO:要検討 
        # ヤフオクアカウントIDが未指定の場合(GET時)
        if yahoo_account_id == None:
            self.torihiki_data_table1=TorihikiTable(TorihikiModel.objects.filter(account_id=self.request.user, yahoo_account_id=None))
            self.torihiki_data_table2=TorihikiTable(TorihikiModel.objects.filter(account_id=self.request.user, yahoo_account_id=None))
            self.torihiki_data_table3=TorihikiTable(TorihikiModel.objects.filter(account_id=self.request.user, yahoo_account_id=None))
            self.torihiki_data_table4=TorihikiTable(TorihikiModel.objects.filter(account_id=self.request.user, yahoo_account_id=None))
            self.torihiki_data_table5=TorihikiTable(TorihikiModel.objects.filter(account_id=self.request.user, yahoo_account_id=None))
            self.record_count1=0
            self.record_count2=0
            self.record_count3=0
            self.record_count4=0
            self.record_count5=0
        else:   
            # 取引開始前
            self.torihiki_data1=TorihikiModel.objects.filter(account_id=self.request.user,torihiki_stat=0,yahoo_account_id=yahoo_account_id)
            self.record_count1=self.torihiki_data1.count() # 件数取得
            # 取引ステータスの変換
            #for i,data in enumerate(torihiki_data1):
            #    torihiki_data[i].torihiki_stat=CONST.TORIHIKI_STAT[str(data.torihiki_stat)]
            self.torihiki_data_table1=TorihikiTable(self.torihiki_data1.order_by("-rakusatsu_at")) #テーブルに格納
            
            # 支払い前
            self.torihiki_data2=TorihikiModel.objects.filter(account_id=self.request.user,torihiki_stat=1,yahoo_account_id=yahoo_account_id)
            self.record_count2=self.torihiki_data2.count() # 件数取得
            self.torihiki_data_table2=TorihikiTable(self.torihiki_data2.order_by("-rakusatsu_at")) #テーブルに格納
            
            # 発送前
            self.torihiki_data3=TorihikiModel.objects.filter(account_id=self.request.user,torihiki_stat=2,yahoo_account_id=yahoo_account_id)
            self.record_count3=self.torihiki_data3.count() # 件数取得
            self.torihiki_data_table3=TorihikiTable(self.torihiki_data3.order_by("-rakusatsu_at")) #テーブルに格納
            
            # 受け取り前
            self.torihiki_data4=TorihikiModel.objects.filter(account_id=self.request.user,torihiki_stat=3,yahoo_account_id=yahoo_account_id)
            self.record_count4=self.torihiki_data4.count() # 件数取得
            self.torihiki_data_table4=TorihikiTable(self.torihiki_data4.order_by("-rakusatsu_at"), orderable=False) #テーブルに格納
            
            # 取引完了
            self.torihiki_data5=TorihikiModel.objects.filter(account_id=self.request.user,torihiki_stat=4,yahoo_account_id=yahoo_account_id)
            print(self.torihiki_data5)
            self.record_count5=self.torihiki_data5.count() # 件数取得
            self.torihiki_data_table5=TorihikiTable(self.torihiki_data5.order_by("-rakusatsu_at")) #テーブルに格納
            
