#coding=utf-8
#-----------------------------------------------------------------
# 提取函数和函数参数
#-----------------------------------------------------------------

import explain_fun_param as efp  # 提取函数参数子库
import sys
# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast, parse_file

# 查看函数调用的类
class FuncCall_Visitor(c_ast.NodeVisitor):
    def visit_FuncCall(self, node): 
        #print(type(node))
        print("    " + node.name.name)

# 查看函数定义的类
class FuncDefVisitor(c_ast.NodeVisitor):
    # 查看 函数定义
    def visit_FuncDef(self, node):
        print(type(node))
        
# 显示函数定义的信息
def show_func_def(ast):
    try:
        for nd in ast.ext:
            if type(nd) == c_ast.FuncDef:
                
                # 显示函数名、参数数量、位置等
                print("func: %s , loc: %s " % (nd.decl.name, nd.decl.coord))
                
                # 描述函数参数
                print("  param:")
                try:
                    for i in range(len(nd.decl.type.args.params)):
                        desc = efp.explain_c_declaration(nd.decl.type.args.params[i],ast,expand_struct=True,expand_typedef=True)
                        print("    %d: %s " % (i+1, desc))
                        desc_list = desc.split(' ')
                        if desc_list[3] not in ['pointer','array','struct','function']:
                            print "       " + " ".join(desc_list[3:]) # 类型
                        else:
                            print "       " + desc_list[3]
                except:
                    print("    no param")
                # 描述函数返回值类型
                print("  func return type:")
                print("    %s " %(efp._explain_type(nd.decl.type.type)))
                
                # 描述函数内部的函数调用
                print("  func call:")
                #v = FuncCall_Visitor()
                #v.visit(nd) 
                # 函数体
                function_body = nd.body
                try:
                    func_call_num = 0
                    for decl in function_body.block_items:
                        # 函数体内的每一个子节点 
                        if type(decl) == c_ast.FuncCall:
                            #decl.show()
                            func_call_num += 1
                            print("    %d: %s " % (func_call_num, decl.name.name))
                    if func_call_num == 0:
                        print("    no func call")
                except:
                    print("    no func call")
    except:
        print("ast has 0 node")
        
def show_func_call_tree(str_main_func, ast):
    call_tree_dict = {}
    call_tree_dict[str_main_func] = {}
    try:
        for nd in ast.ext:
            # 从指定的函数节点开始寻找
            if type(nd) == c_ast.FuncDef and str_main_func == nd.decl.name:
                function_body = nd.body
                try:
                    func_call_num = 0
                    for decl in function_body.block_items:
                        # 函数体内的每一个子节点 
                        if type(decl) == c_ast.FuncCall:
                            #decl.show()
                            func_call_num += 1
                            #print("    %d: %s " % (func_call_num, decl.name.name))
                            call_tree_dict[str_main_func][decl.name.name]={}
                    if func_call_num == 0:
                        print("    no func call")
                except:
                    print("    no func call")
    except:
        print("ast has 0 node")
    return call_tree_dict
    
def print_func_call_tree(call_tree_dict,cnt=1):
    for key in call_tree_dict:
        print("  " + key)
        print_func_call_tree(call_tree_dict[key],)
    
# 显示函数信息 和 调用树
def show_func(filename):

    use_cpp=True # 执行预处理 execute the C pre-processor  可以去除注释  和 宏定义等
    #use_cpp = False
    if use_cpp:
        from pycparser import preprocess_file
        cpp_path = 'cpp'                      # 预处理 器 路径
        cpp_args=r'-Iutils/fake_libc_include' # command line arguments 预处理选项
        text = preprocess_file(filename, cpp_path, cpp_args)
    else:
        import io
        with io.open(filename) as f:
            text = f.read()
            
    if not use_cpp:
        # 去除注释
        import decomment as dc
        rc = dc.rmcmnt("c")
        text, rm = rc.removecomment(text)
        
    parser = c_parser.CParser()
    global ast
    ast = parser.parse(text, filename)
    
    # 显示函数定义的信息
    show_func_def(ast)
    
    # 显示函数调用树
    print("func_call_tree:")
    call_tree_d = show_func_call_tree("main",ast)
    print_func_call_tree(call_tree_d)
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename  = sys.argv[1]
    else:
        filename = '../examples/c_files/hash.c'
    show_func(filename)
