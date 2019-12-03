#coding:utf-8
# 解析函数参数(描述函数参数)
#-----------------------------------------------------------------
# 
#-----------------------------------------------------------------
import copy
import sys

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast


def explain_c_declaration(dest_node, father_node, expand_struct=False, expand_typedef=False):
    """ Parses the declaration in dest_node and returns a text
        explanation as a string.
        dest_node is the target node.
        father_node is the father node, may contain the struct/typedef define.
        expand_struct=True will spell out struct definitions recursively.
        expand_typedef=True will expand typedef'd types.
    """
    try:
        # 展开结构体 和类型定义
        expanded = expand_struct_typedef(dest_node, father_node,
                                         expand_struct=expand_struct,
                                         expand_typedef=expand_typedef)
    except Exception as e:
        return "Not a valid declaration: " + str(e)
    
    # 描述 定义
    return _explain_decl_node(expanded)

    # 解释声明节点
def _explain_decl_node(decl_node):
    """ Receives a c_ast.Decl note and returns its explanation in
        English.
    """
    # 变量所处内存方式 static静态局部  extern扩展全局 register寄存器变量
    storage = ' '.join(decl_node.storage) + ' ' if decl_node.storage else ''
    
    # 节点名字  是一个  存储方式
    return (decl_node.name +
            " is a " +
            storage +
            _explain_type(decl_node.type))

# 解释声明节点的类型
def _explain_type(decl):
    """ Recursively explains a type decl node
    """
    
    # 声明节点的类型 类型声明TypeDecl / 类型名Typename / 声明父节点Decl /  标识符类型IdentifierType / 指针声明PtrDecl / 数组声明ArrayDecl / 函数声明FuncDecl / 结构体Struct
    typ = type(decl)

    if typ == c_ast.TypeDecl:
        # 加上限定符 qualifiers : const常量  volatile易变量
        quals = ' '.join(decl.quals) + ' ' if decl.quals else ''
        # 递归解释其类型
        return quals + _explain_type(decl.type)
        
    # 类型名Typename / 声明父节点Decl 
    elif typ == c_ast.Typename or typ == c_ast.Decl:
        return _explain_type(decl.type)
        
    # 最后层 标识符类型  int/float/char/...
    elif typ == c_ast.IdentifierType:
        return ' '.join(decl.names)
    
    # 指针声明
    elif typ == c_ast.PtrDecl:
        quals = ' '.join(decl.quals) + ' ' if decl.quals else ''
        return quals + 'pointer to ' + _explain_type(decl.type)
    
    # 数组声明 
    elif typ == c_ast.ArrayDecl:
        arr = 'array'
        if decl.dim: # 有数组大小信息
             arr += '[%s]' % decl.dim.value
        return arr + " of " + _explain_type(decl.type)
    
    # 函数声明
    elif typ == c_ast.FuncDecl:
        # 递归解析 函数的参数
        if decl.args:
            params = [_explain_type(param) for param in decl.args.params] # ? 函数的参数不是一个定义吗  (没有 存储方式标识)
            args = ', '.join(params)
        else:
            args = ''
        
        # 加上函数的返回值类型
        return ('function(%s) returning ' % (args) +
                _explain_type(decl.type))
    
    # 结构体
    elif typ == c_ast.Struct:
        # 解析每一个结构体成员
        decls = [_explain_decl_node(mem_decl) for mem_decl in decl.decls]
        members = ', '.join(decls)
        
        # 加上结构体的名字
        return ('struct%s ' % (' ' + decl.name if decl.name else '') +
                ('containing {%s}' % members if members else ''))


def expand_struct_typedef(cdecl, file_ast,
                          expand_struct=False,
                          expand_typedef=False):
    """Expand struct & typedef and return a new expanded node."""
    decl_copy = copy.deepcopy(cdecl)
    # 原node上展开
    _expand_in_place(decl_copy, file_ast, expand_struct, expand_typedef)
    return decl_copy


def _expand_in_place(decl, file_ast, expand_struct=False, expand_typedef=False):
    """Recursively expand struct & typedef in place, throw RuntimeError if
       undeclared struct or typedef are used
    """
    typ = type(decl) # 最后一个节点的类型
    
    # 声明父类、类型声明子类、指针声明子类、数组声明子类  直接跳过 递归处理
    if typ in (c_ast.Decl, c_ast.TypeDecl, c_ast.PtrDecl, c_ast.ArrayDecl):
        decl.type = _expand_in_place(decl.type, file_ast, expand_struct,
                                     expand_typedef)
    
    #结构体类型
    elif typ == c_ast.Struct:
        # 是一个结构体，但是未有定义，定义在之前的节点中有
        if not decl.decls:
            struct = _find_struct(decl.name, file_ast) # 在文件ast中找之前定义的结构体
            if not struct:
                raise RuntimeError('using undeclared struct %s' % decl.name)
            decl.decls = struct.decls
        
        # 展开 结构体的 变量
        for i, mem_decl in enumerate(decl.decls):
            # 展开结构体内部的  每一个成员的 定义   递归处理
            decl.decls[i] = _expand_in_place(mem_decl, file_ast, expand_struct,
                                             expand_typedef)
                                             
        # 如果不需要扩展 结构体 把 结构体的定义清空
        if not expand_struct:
            decl.decls = []
    
    # 标识符类型
    elif (typ == c_ast.IdentifierType and
          decl.names[0] not in ('int', 'char', 'float', 'unsigned', 'signed', 'double')):
        typedef = _find_typedef(decl.names[0], file_ast)
        if not typedef:
            raise RuntimeError('using undeclared type %s' % decl.names[0])

        if expand_typedef:
            return typedef.type  # 类型定义

    return decl


def _find_struct(name, file_ast):
    """Receives a struct name and return declared struct object in file_ast
    """
    if file_ast.ext:
        for node in file_ast.ext:
            if (type(node) == c_ast.Decl and
               type(node.type) == c_ast.Struct and
               node.type.name == name):
                return node.type


def _find_typedef(name, file_ast):
    """Receives a type name and return typedef object in file_ast
    """
    if file_ast.ext:
        for node in file_ast.ext:
            if type(node) == c_ast.Typedef and node.name == name:
                return node 
                
                
