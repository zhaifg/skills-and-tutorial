# 自定义admin
---


# kingadmin  的 后台注册
enables_plugins = {
    "crm": {
        
    }
}

site.register 注册就是 

site

class AdminSite(object):
    def  __init__(self)

    def register(self, model_class, admin_class=None):


site = AdminSite()


.table_change
def table_obj_change(request, app_name, model_name, obj_id):
    pass


使用ModelForm, 动态ModelForm , 动态生成类: 元类

class Meta:
     dfasd
def careate_dynamic_model_form(admin_class):
    """动态生成ModelForm"""
    dynamic_form = type("DynamicModelForm", (ModelForm,), {"Meta": Meta})

    ready_only 字段


filter_horizontal 字段
